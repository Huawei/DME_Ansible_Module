# -*- coding: utf-8
from hw_dme_ansible_core import param_base


def main():
    # 获取命令参数，入参为该业务必须的参数字段
    token, param = param_base.get_param('name')
    client = param_base.ParamIR(token)
    # 根据业务，通过client 请求，并组装参数返回
    result = []
    name = param.get('name')
    logic_ip = param.get('logic_ip')
    storage_infos = client.get(
        '/rest/storagemgmt/v1/storages?start=1&limit=100').get(
        'datas')

    for info in storage_infos:
        req_param = {'storage_id': info.get('id'), 'page_no': 1,
                     'page_size': 100}
        pool_info = client.post(
            '/rest/storagemgmt/v1/storagepools/query', req_param).get("datas")
        total = 0
        for pool in pool_info:
            total += pool['total_capacity']
        if total == 0:
            continue
        info['usableCapacity'] = total

        body = {'page_no': 1, 'page_size': 10, 'name': name,
                'storage_id': info.get('id')}
        file_info = client.post('/rest/fileservice/v1/filesystems/query', body)
        if file_info.get('total') == 0:
            continue
        if not check_logic_port(logic_ip, client, info.get('id')):
            continue
        result.append(
            {'name': param_base.get_storage_result(info),
             'value': info.get('id')})
    print(result)


def check_logic_port(logic_ip, client, storage_id):
    if not len(logic_ip) == 0:
        req_param = {'storage_id': storage_id}
        logic_ports_infos = client.post(
            '/rest/storagemgmt/v1/logic-ports/query', req_param).get(
            'logic_ports')
        logic_ports = []
        for logic_ports_info in logic_ports_infos:
            logic_ports.append(logic_ports_info.get('mgmt_ip'))
        if logic_ip in logic_ports:
            return True
        else:
            return False
    else:
        return True


if __name__ == '__main__':
    try:
        main()
    except param_base.ScriptException:
        print([])
