# -*- coding: utf-8
from hw_dme_ansible_core import param_base


def main():
    # 获取命令参数，入参为该业务必须的参数字段
    token, param = param_base.get_param('fs_id')
    client = param_base.ParamIR(token)
    # 根据业务，通过client 请求，并组装参数返回
    fs_id = param.get('fs_id')
    nfs_id = param.get('nfs_id')
    add_client_r = param.get('add_client_r')
    add_client_rw = param.get('add_client_rw')
    delete_client_id_str = param.get('delete_client_id')
    delete_client_ids = []
    result = []
    if delete_client_id_str:
        delete_client_ids = delete_client_id_str.split(',')
    file_info = client.get(
        '/rest/fileservice/v1/filesystems/' + fs_id)
    value = '文件系统名称：' + file_info.get(
        'name') + '；\n所属存储设备：' + file_info.get(
        'storage_name') + '；\n所属存储池：' + file_info.get(
        'storage_pool_name') + '；'
    add_client_num = 0
    if add_client_r or add_client_rw:
        value += '\n新增客户端：'
        if add_client_r:
            value += add_client_r + '(R)；'
            add_client_num += len(add_client_r.split(','))
        if add_client_rw:
            value += add_client_rw + '(RW)；'
            add_client_num += len(add_client_rw.split(','))

    client_infos = get_clients(client, nfs_id)
    if param.get('delete_client').lower() == 'true' and len(delete_client_ids) > 0:
        value += get_delete_client(client_infos, delete_client_ids)

    value += '\n修改后文件系统访问客户端数量{}个。'.format(add_client_num + len(client_infos) - len(delete_client_ids))
    result.append({'message': value})
    print(result)


def get_clients(client, nfs_id):
    body = {'page_no': 1, 'page_size': 100, 'nfs_share_id': nfs_id}
    info = client.post('/rest/fileservice/v1/nfs-auth-clients/query',
                       body)
    page_size = info.get('total')
    client_infos = []
    if page_size <= 100:
        client_infos = info.get('auth_client_list')
    else:
        body['page_size'] = page_size
        client_infos = client.post(
            '/rest/fileservice/v1/nfs-auth-clients/query',
            body).get('auth_client_list')
    return client_infos


def get_delete_client(client_infos, delete_client_ids):
    value = '\n移除客户端：'
    for delete_client_id in delete_client_ids:
        value += get_client_info(client_infos, delete_client_id)
    return value


def get_client_info(client_infos, delete_client_id):
    for client_info in client_infos:
        client_name = client_info.get('name')
        client_id = client_info.get('client_id_in_storage')
        permission = client_info.get('permission')
        per = 'R' if permission == 'read-only' else 'RW'
        if client_id == delete_client_id:
            return client_name + '(' + per + ')；'


if __name__ == '__main__':
    try:
        main()
    except param_base.ScriptException:
        print([])
