# -*- coding: utf-8
from hw_dme_ansible_core import param_base


def main():
    # 获取命令参数，入参为该业务必须的参数字段
    token, param = param_base.get_param('fs_id')
    client = param_base.ParamIR(token)
    # 根据业务，通过client 请求，并组装参数返回
    result = []
    fs_id = param.get('fs_id')
    new_capacity = param.get('new_capacity')
    unit = param.get('capacity_unit')
    file_info = client.get(
        '/rest/fileservice/v1/filesystems/' + fs_id)
    mes = '文件系统名称：' + file_info.get(
        'name') + '；\n所属存储设备：' + file_info.get(
        'storage_name') + '；\n所属存储池：' + file_info.get(
        'storage_pool_name') + '；\n文件系统原容量' + param_base.get_capacity(
        file_info.get('capacity')) + '；'
    if not len(new_capacity) == 0:
        mes += "\n新容量为" + str(new_capacity) + unit + '。'
    result.append({'message': mes})
    print(result)


if __name__ == '__main__':
    try:
        main()
    except param_base.ScriptException:
        print([])
