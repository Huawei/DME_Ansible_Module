# -*- coding: utf-8
import json
import urllib.parse

from hw_dme_ansible_core import param_base

ETH_BOND_WIDTH_OBJ = '1125925676646400'
ETH_BOND_WIDTH_VAL = '1125925676711981'
AVG_NFS_BOND_WIDTH = '0'
LOGIC_PORT_BOND_WIDTH_OBJ = '1126187669651456'
LOGIC_PORT_BOND_WIDTH_VAL = '1126187669651457'


def main():
    # 获取命令参数，入参为该业务必须的参数字段
    token, param = param_base.get_param('storage_id', 'add_client_ips_r',
                                        'add_client_ips_rw')
    client = param_base.ParamIR(token)
    # 根据业务，通过client 请求，并组装参数返回
    req_param = {'storage_id': param['storage_id']}
    logic_ports = client.post(
        '/rest/storagemgmt/v1/logic-ports/query', req_param).get('logic_ports')

    logic_ports_info = [logic_port for logic_port in logic_ports if
                        logic_port.get(
                            'support_protocol') == 'NFS_AND_CIFS' or logic_port.get(
                            'support_protocol') == 'NFS']
    logic_ports_with_ids = {}
    for port in logic_ports_info:
        logic_ports_with_ids[port['mgmt_ip']] = port

    # 根据ip过滤
    datas = filter_by_ip(logic_ports_info, logic_ports_with_ids, param)

    # 查询当前设备所有以太网端口
    eth_ports = query_eth_port(client, param)
    all_ports = query_all_port(client, param)
    # 查询所有端口性能数据
    all_ports_ids = []
    for port in all_ports:
        all_ports_ids.append(port['id'])
    all_performances_with_ids = query_performance(client, all_ports_ids,
                                                  ETH_BOND_WIDTH_OBJ,
                                                  ETH_BOND_WIDTH_VAL)

    # 以太网匹配所有端口controllId==nativeId获取多个id
    eth_ports_with_name = eth_port_with_per(all_performances_with_ids,
                                            all_ports, eth_ports)

    # 查询当前设备所有绑定端口
    bond_ports = query_bond_port(client, param)
    # 收集绑定端口端口{名称：绑定端口}
    bond_ports_with_name = {}
    for port in bond_ports:
        bond_ports_with_name[port['name']] = port

    new_datas = match_logic_port_per(bond_ports_with_name, client, datas,
                                     eth_ports_with_name)

    new_datas = sorted(new_datas, key=lambda x: (x.get('used_ratio')),
                       reverse=True)
    result = []
    for info in new_datas:
        if info['used_ratio'] == '--':
            used_ratio = str(info['used_ratio']) + ')'
        else:
            used_ratio = str(info['used_ratio']) + '%)'
        value = info.get('name') + '(IP地址：' + info.get('mgmt_ip') + '，带宽利用率：' + used_ratio
        result.append({'value': info['id'], 'name': value})
    print(result)


def query_bond_port(client, param):
    bond_ports = []
    try:
        bond_ports = client.post(
            '/rest/storagemgmt/v1/bond-ports/query',
            {'storage_id': param.get('storage_id')}).get('bond_ports')
    except Exception:
        pass
    return bond_ports


def match_logic_port_per(bond_ports_with_name, client, datas,
                         eth_ports_with_name):
    new_datas = []
    for logic_port in datas:
        logic_id = [logic_port['id']]
        logic_performance = query_performance(client, logic_id,
                                              LOGIC_PORT_BOND_WIDTH_OBJ,
                                              LOGIC_PORT_BOND_WIDTH_VAL)
        if logic_port.get('current_port_type') == 'ETHERNET_PORT':
            # 逻辑端口中主用端口为以太口时候，利用率=逻辑端口带宽/以太口工作速率
            logic_port = match_eth(eth_ports_with_name, logic_port, logic_performance)
            new_datas.append(logic_port)
        elif logic_port.get('current_port_type') == 'BOND':
            # 查询逻辑端口nfs带宽
            # 逻辑端口主用端口是绑定端口时候，利用率=逻辑端口带宽/sum（以太网口工作速率）
            if len(logic_performance) == 0:
                logic_port['used_ratio'] = '--'
                new_datas.append(logic_port)
                continue
            current_port_name = logic_port.get('current_port_name')
            if bond_ports_with_name.get(current_port_name):
                bond_id = bond_ports_with_name.get(current_port_name).get('id')
                # 绑定端口
                match_bond(bond_id, client, logic_port, logic_performance)
            else:
                logic_port['used_ratio'] = '--'
            new_datas.append(logic_port)

    return new_datas


def match_bond(bond_id, client, logic_port, logic_performance):
    bond_eth_ports = client.get(
        '/rest/storagemgmt/v1/bond-ports/' + bond_id + '/eth-ports').get(
        'eth_ports')
    if bond_eth_ports:
        sum_speed = 0
        for bond_eth_port in bond_eth_ports:
            sum_speed = sum_speed + bond_eth_port['speed']
        # logic_bond_width逻辑端口返回带宽单位KB/s
        # sum_speed绑定端口下以太端口工作速率Gbit/s
        logic_bond_width = \
            logic_performance[logic_port['id']][LOGIC_PORT_BOND_WIDTH_VAL][
                'avg'][
                AVG_NFS_BOND_WIDTH]
        width_bond_gb = float(logic_bond_width) * 8 / 1024 / 1024
        sum_gb = float(sum_speed) / 1000
        logic_port['used_ratio'] = format(
            abs(width_bond_gb / sum_gb) * 100, '.3f')
    else:
        logic_port['used_ratio'] = '--'


def match_eth(eth_ports_with_name, logic_port, logic_performance):
    current_port_name = logic_port['current_port_name']
    # 以太网端口
    eth_port = eth_ports_with_name.get(current_port_name)
    # 计算利用率
    if eth_port and eth_port.get('speed'):
        speed = eth_port['speed']
        logic_width = logic_performance[logic_port['id']][LOGIC_PORT_BOND_WIDTH_VAL]['avg'][AVG_NFS_BOND_WIDTH]
        if logic_width:
            # logic单位是kb，以太端口速度Mbit/s，利用率=逻辑端口带宽/以太口工作速率
            used_ratio = format(abs(float(logic_width) * 8 / 1024 / speed * 100), '.3f')
            logic_port['used_ratio'] = used_ratio
        else:
            logic_port['used_ratio'] = '--'
    else:
        logic_port['used_ratio'] = '--'
    return logic_port


def eth_port_with_per(all_performances_with_ids, all_ports, eth_ports):
    eth_ports_new = []
    for port in eth_ports:
        for all_port in all_ports:
            if port['nativeId'] == all_port['nativeId'] and len(
                    all_performances_with_ids) > 0:

                if all_performances_with_ids.get(all_port.get('id')):
                    port['performance'] = all_performances_with_ids.get(
                        all_port.get('id'))
                    break
        eth_ports_new.append(port)
    # 收集以太网端口{名称：以太网}
    eth_ports_with_name = {}
    for port in eth_ports_new:
        eth_ports_with_name[port['slot']] = port
    return eth_ports_with_name


def query_eth_port(client, param):
    eth_ports = json.loads(
        client.get(
            '/rest/storagemgmtservice/v1/storages/ethports?neId=' + param[
                'storage_id'] + '&offset=1&limit=100').get('data'))
    return eth_ports


def filter_by_ip(logic_ports_info, logic_ports_with_ids, param):
    client_ips_r = ''
    if param['add_client_ips_r']:
        client_ips_r = param['add_client_ips_r']
    client_ips_rw = ''
    if param['add_client_ips_rw']:
        client_ips_rw = param['add_client_ips_rw']
    ips_params = param_base.get_ip_b(
        ('{},{}'.format(client_ips_r, client_ips_rw)).split(','))
    datas = ()
    for key in logic_ports_with_ids:
        if set(param_base.get_ip_b([key])).issubset(set(ips_params)):
            datas = datas + (logic_ports_with_ids[key],)
    if len(datas) == 0 or len(set(ips_params)) > 1:
        datas = logic_ports_info
    return datas


def query_all_port(client, param):
    # 查询所有端口
    condition = '{\"constraint\":[{\"simple\":{\"name\":\"nativeId\",\"value\":' \
                '\"nedn=' + param[
                    'storage_id'] + ',\",\"operator\":\"begin with\"}},' \
                                    '{\"logOp\":\"and\",\"simple\":{\"name\":\
                                    "dataStatus\",\"value\":\"normal\"}}]}'
    condition = urllib.parse.urlencode({'condition': condition})
    # 查询所有端口
    all_ports = client.get(
        '/rest/csm-cmdb/v1/instances/SYS_StoragePort?' + condition + '&pageSize=1000&pageNo=1').get(
        'objList')
    return all_ports


def list_split(items, n):
    return [items[i:i + n] for i in range(0, len(items), n)]


def query_performance(client, indicator_ids, obj_type_id, obj_type_val):
    id_list = list_split(indicator_ids, 5)
    result = {}
    for ids in id_list:
        performances_param = {'interval': 'HALF_HOUR',
                              'range': 'LAST_1_WEEK',
                              'obj_type_id': obj_type_id,
                              'indicator_ids': [obj_type_val],
                              'obj_ids': ids}
        # 查询性能
        data = client.post(
            '/rest/performance/v1/data-svc/history-data/action/query',
            performances_param).get('data')
        for key in data.keys():
            if data[key].get(ETH_BOND_WIDTH_VAL):
                data[key][ETH_BOND_WIDTH_VAL]['series'] = []
            if data[key].get(LOGIC_PORT_BOND_WIDTH_VAL):
                data[key][LOGIC_PORT_BOND_WIDTH_VAL]['series'] = []
            result[key] = data[key]
    return result


if __name__ == '__main__':
    try:
        main()
    except param_base.ScriptException:
        print([])
