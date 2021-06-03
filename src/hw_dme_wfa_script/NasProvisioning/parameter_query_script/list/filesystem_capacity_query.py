# -*- coding: utf-8
from hw_dme_ansible_core import param_base


def main():
    # 获取命令参数，入参为该业务必须的参数字段
    token, param = param_base.get_param('fs_id')
    client = param_base.ParamIR(token)
    # 根据业务，通过client 请求，并组装参数返回
    result = []
    fs_id = param.get('fs_id')
    file_info = client.get(
        '/rest/fileservice/v1/filesystems/' + fs_id)

    result.append({'value': file_info.get('id'),
                   'name': param_base.get_capacity(file_info.get('capacity'))})
    print(result)


if __name__ == '__main__':
    try:
        main()
    except param_base.ScriptException:
        print([])
