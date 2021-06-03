# -*- coding: utf-8
from hw_dme_ansible_core import param_base


def main():
    # 获取命令参数，入参为该业务必须的参数字段
    token, param = param_base.get_param('storage_id')
    client = param_base.ParamIR(token)
    # 查询存储池
    storage_id = param.get('storage_id')
    fs_id = param.get('fs_id')

    storage_pool_name = client.get(
        '/rest/fileservice/v1/filesystems/' + fs_id).get('storage_pool_name')
    body = {'storage_id': storage_id, 'page_no': 1,
            'page_size': 100}
    storage_info = client.post('/rest/storagemgmt/v1/storagepools/query', body)
    datas = storage_info.get('datas')
    result = []
    for info in datas:
        if storage_pool_name == info.get('name'):
            result.append({'value': info.get('name'),
                           'name': param_base.get_storage_pool_result(info)})
    print(result)


if __name__ == '__main__':
    try:
        main()
    except param_base.ScriptException:
        print([])
