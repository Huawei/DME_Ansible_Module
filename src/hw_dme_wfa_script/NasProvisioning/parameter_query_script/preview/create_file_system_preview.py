# -*- coding: utf-8

from hw_dme_ansible_core import param_base


def main():
    # 获取命令参数，入参为该业务必须的参数字段
    token, param = param_base.get_param('storage_id')
    client = param_base.ParamIR(token)
    # 根据业务，通过client 请求，并组装参数返回
    storage_id = param.get('storage_id')
    storage_info = param_base.get_storage_info(client, storage_id)
    pool_list = get_pool_list(client, storage_id)
    storage_view = get_storage_view(pool_list, storage_info)

    # 存储池
    # 查询存储池
    pool_view = '--'
    for info in pool_list:
        if str(info['storage_pool_id']) == str(param['pool_id']):
            pool_view = param_base.get_storage_pool_result(info)
    ips = client_data(param)
    share_view = ''
    for ip in ips:
        share_view = share_view + ip + ':/' + param['name'] + '/;'
    if share_view != '':
        share_view = share_view[:-1] + ''
    if param_base.is_dorado_device(storage_info):
        value = nas_view(param, pool_view, share_view, storage_view)
    else:
        value = not_nas_view(param, pool_view, share_view, storage_view)
    print([{'message': value}])


def get_storage_view(pool_info, storage_info):
    total = 0
    for pool in pool_info:
        total += pool['total_capacity']
    storage_info['usableCapacity'] = total
    if total == 0:
        return storage_info.get('name') + '(剩余容量：--，已分配：--)'
    subscription_capacity = storage_info.get('subscription_capacity')
    used_capacity_radio = format(subscription_capacity / total, '.0%')
    remaining_capacity = int(total - subscription_capacity)
    storage_view = storage_info.get('name') + '(剩余容量：' + param_base.get_capacity(
        remaining_capacity) + '，已分配：' + str(
        used_capacity_radio) + ')'
    return storage_view


def get_pool_list(client, storage_id):
    req_param = {'storage_id': storage_id, 'page_no': 1,
                 'page_size': 100}
    pool_info = client.post(
        '/rest/storagemgmt/v1/storagepools/query', req_param).get("datas")
    return pool_info


def client_data(param):
    ips = []
    if param.get('add_client_ips_rw'):
        add_client_ips_rw = param['add_client_ips_rw'].split(',')
        for ip in add_client_ips_rw:
            if ip:
                ips.append(ip)
    if param.get('add_client_ips_r'):
        add_client_ips_r = param['add_client_ips_r'].split(',')
        for ip in add_client_ips_r:
            if ip:
                ips.append(ip)
    return ips


def nas_view(param, pool_view, share_view, storage_view):
    name = param.get('name')
    add_client_ips_r = param.get('add_client_ips_r')
    add_client_ips_rw = param.get('add_client_ips_rw')
    capacity = param.get('capacity')
    units = build_units(param)
    value = ''
    value += '存储设备{}，'.format(storage_view)
    value += '存储池{}；\n'.format(pool_view)

    if name:
        value += '文件系统名称{}，'.format(name)
    if capacity:
        value += '文件系统容量为{}{}，'.format(capacity, units)

    value += '快照目录不可见，'
    value += '容量告警阈值为80%；\n'
    if name:
        value += '共享类型：NFS，共享路径 /{}/，'.format(name)
    if share_view:
        value += '共享描述（{}），'.format(share_view)
    value += 'root权限限制为no_root_squash，字符编码为UTF-8。'

    if add_client_ips_r:
        value += '共享客户端{}权限为只读（数量为{}），'.format(add_client_ips_r, len(add_client_ips_r.split(',')))
    if add_client_ips_rw:
        value += '共享客户端{}权限为读写（数量为{}）。'.format(add_client_ips_rw, len(add_client_ips_rw.split(',')))
    value = value[:-1] + '。'
    return value


def build_units(param):
    if param['units'] == 'TB':
        return 'TB'
    else:
        return 'GB'


def not_nas_view(param, pool_view, share_view, storage_view):
    name = param.get('name')
    add_client_ips_r = param.get('add_client_ips_r')
    add_client_ips_rw = param.get('add_client_ips_rw')
    snapshot_reserved_space_percentage = param.get(
        'snapshot_reserved_space_percentage')
    capacity = param.get('capacity')
    units = build_units(param)
    value = ''
    value += '存储设备{}，'.format(storage_view)
    value += '存储池{}；\n'.format(pool_view)
    if name:
        value += '文件系统名称{}，'.format(name)

    value += '类型为Thick，'
    if capacity:
        value += '容量为{}{}，'.format(capacity, units)
    value += '文件系统块大小为4K，'
    if param['open_dr'] == 'true':
        value += '快照空间比例为{}%，'.format(snapshot_reserved_space_percentage)
    else:
        value += '快照空间比例为{}%，'.format(0)
    value += '快照目录不可见，定时快照数量上限为1;\n'
    if name:
        value += '共享路径 /{}/，'.format(name)
    if share_view:
        value += '共享描述（{}），显示Snapshot:不启用，'.format(share_view)
    value += 'root权限限制为no_root_squash，字符编码为UTF-8;'
    if add_client_ips_r:
        value += '\n共享客户端{}权限为只读，'.format(add_client_ips_r)
        if add_client_ips_rw:
            value += '共享客户端{}权限为读写。'.format(add_client_ips_rw)
    elif add_client_ips_rw:
        value += '\n共享客户端{}权限为读写。'.format(add_client_ips_rw)
    value = value[:-1] + '。'
    return value


if __name__ == '__main__':
    try:
        main()
    except param_base.ScriptException:
        print([])
