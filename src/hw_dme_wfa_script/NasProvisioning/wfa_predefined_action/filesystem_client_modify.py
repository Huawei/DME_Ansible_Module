# -*- coding: utf-8
import json
import datetime
from base import log
from hw_dme_ansible_core import common
from wfa_predefined_action import base
from hw_dme_ansible_core.common import ScriptException


def main():
    # 获取命令参数，入参为该业务必须的参数字段
    param = base.get_param()
    base.init_client(param)
    # 根据业务，通过client 请求，并组装参数返回
    add_todo = param.get('todo')
    nfs_id = param.get('nfs_id')
    add_client_r = param.get('add_client_r')
    add_client_rw = param.get('add_client_rw')
    delete_client_id_str = param.get('delete_client_id')
    delete_client_ids = []
    if delete_client_id_str is not None:
        delete_client_ids = delete_client_id_str.split(',')
    nfs_share_client_deletion = []
    nfs_share_client_addition = []
    if len(delete_client_ids) > 0 and delete_client_ids[0].lower() == 'true':
        for i in range(1, len(delete_client_ids)):
            nfs_share_client_deletion.append(
                {'nfs_share_client_id_in_storage': delete_client_ids[i]})
    if add_client_r:
        for client in add_client_r.split(','):
            if add_client_r is not None:
                nfs_share_client_addition.append(
                    get_add_client(client, "read-only"))
    if add_client_rw:
        for client in add_client_rw.split(','):
            if add_client_rw is not None:
                nfs_share_client_addition.append(
                    get_add_client(client, "read/write"))

    nfs_info = json.loads(base.get(
        '/rest/fileservice/v1/nfs-shares/' + nfs_id)[1])
    body = {"description": nfs_info.get('description'),
            "character_encoding": nfs_info.get('character_encoding'),
            "nfs_share_client_addition": nfs_share_client_addition,
            "nfs_share_client_modification": [],
            "nfs_share_client_deletion": nfs_share_client_deletion}
    if add_todo == 'true':
        todobody = {"name": "modify" + "_client_" + datetime.datetime.now().strftime(
            '%Y%m%d%H%M%S'),
                    "service_type": "update_nfs_share",
                    "request_method": "PUT",
                    "request_uri": "/rest/fileservice/v1/nfs-shares/" + nfs_id,
                    "request_body": json.JSONEncoder().encode(body)}
        create_to_do_items_request_func(todobody)
    else:
        task_id = json.loads(base.put(
            '/rest/fileservice/v1/nfs-shares/' + nfs_id, body)[1])['task_id']
        print(common.check_task(base.task_request, task_id))


@log("create todo items")
def create_to_do_items_request_func(body):
    return base.post("/rest/djbaseomwebsite/v1/todo-items", body)


def get_add_client(add_client_name, permission):
    return {"name": add_client_name, "permission": permission,
            "write_mode": "synchronization",
            "permission_constraint": 'no_all_squash',
            "root_permission_constraint": "root_squash",
            "source_port_verification": "insecure"}


if __name__ == '__main__':
    try:
        main()
    except ScriptException:
        print({})
