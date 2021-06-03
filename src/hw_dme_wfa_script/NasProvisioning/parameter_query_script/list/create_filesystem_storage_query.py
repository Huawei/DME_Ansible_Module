# -*- coding: utf-8

from hw_dme_ansible_core import param_base


def main():
    # 获取命令参数，入参为该业务必须的参数字段
    token, param = param_base.get_param('name', 'file_size', 'add_client_ips_r')
    if not param.get('name') or not param.get('file_size'):
        print([])
        return
    client = param_base.ParamIR(token)
    # 根据业务，通过client 请求，并组装参数返回
    storage_infos = client.get(
        "/rest/storagemgmt/v1/storages?start=1&limit=100").get("datas")

    # 查询逻辑端口
    new_storage_infos = []
    for storage in storage_infos:
        req_param = {'storage_id': storage.get('id'), 'page_no': 1,
                     'page_size': 100}
        pool_info = client.post(
            '/rest/storagemgmt/v1/storagepools/query', req_param).get("datas")
        total = 0
        for pool in pool_info:
            total += pool['total_capacity']
        if total == 0:
            continue
        ips = check_logic_port(client, storage.get('id'))
        storage['ips'] = ips
        storage['usableCapacity'] = total
        new_storage_infos.append(storage)
    # 根据ip过滤
    client_ips_r = param.get('add_client_ips_r')
    client_ips_rw = param.get('add_client_ips_rw')

    ips_params = (
        '{},{}'.format(str(client_ips_r), str(client_ips_rw))).split(',')
    # 取b段
    ips_new = param_base.get_ip_b(ips_params)

    new_datas = filter_and_sort(ips_new, new_storage_infos)
    result = []
    for info in new_datas:
        result.append(
            {'value': info.get('id'),
             'name': param_base.get_storage_result(info)})
    print(result)


def filter_and_sort(ips_new, storage_infos):
    new_datas = []
    for info in storage_infos:
        if info.get('ips'):
            ips = param_base.get_ip_b(info.get('ips'))
        else:
            continue
        # 交集
        if set(ips_new).issubset(set(ips)):
            new_datas.append(info)
    if len(new_datas) == 0:
        new_datas = storage_infos
    # 先排序,已分配）unsort_datas，容量排序（排序规则为：剩余容量（降序）、已分配（升序））
    new_datas.sort(key=lambda x: (
        -(x.get('usableCapacity') - x.get('subscription_capacity')),
        ((x.get('subscription_capacity') / x.get('usableCapacity')))))
    return new_datas


def check_logic_port(client, storage_id):
    req_param = {'storage_id': storage_id}
    logic_ports_info = client.post(
        '/rest/storagemgmt/v1/logic-ports/query', req_param).get(
        'logic_ports')
    logic_ports_ids = [i.get('mgmt_ip') for i in logic_ports_info]
    return logic_ports_ids


if __name__ == '__main__':
    try:
        main()
    except param_base.ScriptException:
        print([])
