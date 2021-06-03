# -*- coding: utf-8
import sys
from hw_dme_ansible_core import param_base


def get_performance(client, fs_id):
    ops_max = "--"
    band_width_max = "--"
    body = {'indicator_ids': ["1126179079716865", "1126179079716878"],
            'interval': "HALF_HOUR", 'obj_ids': [fs_id],
            'obj_type_id': "1126179079716864", 'range': "LAST_1_WEEK"}
    data = client.post(
        '/rest/djstormgmtwebsite/v1/data-svc/history-data/action/query',
        body).get('data')

    if data is not None:
        ops = data.get(fs_id).get('1126179079716865').get('max')
        band_width = data.get(fs_id).get('1126179079716878').get('max')
        for item in ops.keys():
            ops_max = str(ops[item])
        for item in band_width.keys():
            band_width_max = str(band_width[item])
    return ops_max, band_width_max


def build_share_path(client_name, share_path, client, nfs_share_list):
    nfs_share_index = 0
    for nfs_share in nfs_share_list:
        share_path = share_path + nfs_share.get('share_path')
        if (nfs_share_index + 1) != len(nfs_share_list):
            share_path = share_path + "、"
        nfs_share_index = nfs_share_index + 1
        nfs_id = nfs_share.get('id')
        body = {'page_no': 1, 'page_size': 100, 'vstore_id': '0',
                'nfs_share_id': nfs_id}
        client_list = client.post(
            '/rest/fileservice/v1/nfs-auth-clients/query',
            body).get('auth_client_list')
        client_index = 0
        for client_info in client_list:
            client_name = client_name + client_info.get('name')
            if (client_index + 1) != len(client_list):
                client_name = client_name + "、"
            else:
                client_name = client_name + "。"
            client_index = client_index + 1
    return share_path, client_name


def main():
    # 获取命令参数，入参为该业务必须的参数字段
    token, param = param_base.get_param('fs_id')
    if token is None:
        print({})
        sys.exit()
    client = param_base.ParamIR(token)
    # 根据业务，通过client 请求，并组装参数返回
    fs_id = param.get('fs_id')
    fs_info = client.get('/rest/fileservice/v1/filesystems/' + fs_id)
    body = {'page_no': 1, 'page_size': 100, 'fs_id': fs_id}
    nfs_share_list = client.post('/rest/fileservice/v1/nfs-shares/query',
                                 body).get('nfs_share_info_list')

    client_name = ''
    share_path = ''
    if nfs_share_list:
        share_path, client_name = build_share_path(client_name, share_path,
                                                   client, nfs_share_list)
    else:
        client_name = '--。'
        share_path = '--'

    ops_max, band_width_max = get_performance(client, fs_id)
    capacity = param_base.get_capacity(fs_info.get('capacity'))

    value = '最近一周文件系统峰值OPS为' + ops_max + '，' + \
            '文件系统峰值带宽为' + band_width_max + \
            '；\n文件系统名称' + fs_info.get('name') + \
            '；\n所属存储设备' + fs_info.get('storage_name') + \
            '；\n文件系统容量' + capacity + '；\n共享路径为' + share_path + \
            '；\n访问客户端为' + client_name
    print([{'message': value}])


if __name__ == '__main__':
    main()
