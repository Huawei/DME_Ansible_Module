# -*- coding: utf-8

from hw_dme_ansible_core import param_base

BLOCK_AND_FILE_POOL_TYPE = '0'
FILESYSTEM_POOL_TYPE = '2'


def main():
    # 获取命令参数，入参为该业务必须的参数字段
    token, param = param_base.get_param('storage_id')
    client = param_base.ParamIR(token)
    # 查询存储池
    req_param = {'storage_id': param['storage_id'], 'page_no': 1,
                 'page_size': 100}
    pool_info = client.post(
        '/rest/storagemgmt/v1/storagepools/query', req_param)
    unsort_datas = pool_info.get("datas")
    unsort_datas = [info for info in unsort_datas if
                    info.get('usage_type') == FILESYSTEM_POOL_TYPE or info.get(
                        'usage_type') == BLOCK_AND_FILE_POOL_TYPE]
    # 存储池进行容量排序（排序规则为：剩余容量（降序）、已分配（升序））
    unsort_datas.sort(key=lambda x: (
        -(x.get('total_capacity') - x.get('fs_subscribed_capacity')),
        ((x.get('fs_subscribed_capacity') / x.get('total_capacity') / 1024))))
    result = [{'value': info.get('storage_pool_id'),
               'name': param_base.get_storage_pool_result(info)} for info in
              unsort_datas]
    print(result)


if __name__ == '__main__':
    try:
        main()
    except param_base.ScriptException:
        print([])
