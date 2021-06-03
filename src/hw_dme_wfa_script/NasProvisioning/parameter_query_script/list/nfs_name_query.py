# -*- coding: utf-8
from hw_dme_ansible_core import param_base


def main():
    # 获取命令参数，入参为该业务必须的参数字段
    token, param = param_base.get_param('storage_id')
    client = param_base.ParamIR(token)
    # 根据业务，通过client 请求，并组装参数返回
    storage_id = param.get('storage_id')
    fs_id = param.get('fs_id')
    result = []
    body = {'page_no': 1, 'page_size': 1000,
            'storage_id': storage_id, 'fs_id': fs_id}
    info = client.post('/rest/fileservice/v1/nfs-shares/query', body)
    page_size = info.get(
        'total')
    file_infos = []
    if page_size <= 1000:
        file_infos = info.get('nfs_share_info_list')
    else:
        body['page_size'] = page_size
        file_infos = client.post('/rest/fileservice/v1/nfs-shares/query', body).get(
            'nfs_share_info_list')
    for file_info in file_infos:
        result.append(
            {'value': file_info.get('id'), 'name': file_info.get('name')})
    print(result)


if __name__ == '__main__':
    try:
        main()
    except param_base.ScriptException:
        print([])
