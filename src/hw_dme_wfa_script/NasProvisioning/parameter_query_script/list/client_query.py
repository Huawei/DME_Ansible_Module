# -*- coding: utf-8
from hw_dme_ansible_core import param_base


def main():
    # 获取命令参数，入参为该业务必须的参数字段
    token, param = param_base.get_param('nfs_id')
    client = param_base.ParamIR(token)
    # 根据业务，通过client 请求，并组装参数返回
    nfs_id = param.get('nfs_id')
    result = []
    body = {'page_no': 1, 'page_size': 100, 'nfs_share_id': nfs_id}
    page_size = client.post('/rest/fileservice/v1/nfs-auth-clients/query',
                            body).get('total')
    body['page_size'] = page_size
    client_infos = client.post('/rest/fileservice/v1/nfs-auth-clients/query',
                               body).get('auth_client_list')
    for client_info in client_infos:
        client_name = client_info.get('name')
        client_id = client_info.get('client_id_in_storage')
        data = {'name': client_name, 'value': client_id}
        result.append(data)
    print(result)


if __name__ == '__main__':
    try:
        main()
    except param_base.ScriptException:
        print([])
