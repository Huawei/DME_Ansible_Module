# -*- coding: utf-8
import json
import datetime
from base import log
from hw_dme_ansible_core import common
from wfa_predefined_action import base
from hw_dme_ansible_core.common import ScriptException


def main():
    param = base.get_param()
    base.init_client(param)
    # 根据业务，通过client 请求，并组装参数返回
    fs_id = param.get('fs_id')
    new_capacity = param.get('new_capacity')
    add_todo = param.get('todo')
    unit = param.get('capacity_unit')
    if unit == 'TB':
        new_capacity = int(new_capacity) * 1024
    body = {"capacity": new_capacity}
    if add_todo == 'true':
        file_info = json.loads(base.get(
            '/rest/fileservice/v1/filesystems/' + fs_id)[1])
        requestbody = {
            "name": file_info.get('name'),
            "capacity": new_capacity,
            "description": file_info.get('description'),
            "capacity_threshold": file_info.get('capacity_threshold'),
            "initial_distribute_policy": file_info.get(
                'initial_distribute_policy'),
            "security_mode": file_info.get('security_mode'),
            "snapshot_expired_enabled": file_info.get(
                'snapshot_expired_enabled'),
            "checksum_enabled": file_info.get('checksum_enabled'),
            "automatic_update_time": file_info.get('automatic_update_time'),
            "tuning": {
                "qos_policy": {
                    "enabled": False
                }
            }
        }
        todobody = {
            "name": "modify" + "_capacity_" +
                    datetime.datetime.now().strftime(
                        '%Y%m%d%H%M%S'),
            "service_type": "update_filesystem",
            "request_method": "PUT",
            "request_uri": "/rest/fileservice/v1/filesystems/" + fs_id,
            "request_body": json.JSONEncoder().encode(requestbody)}
        create_to_do_items_request_func(todobody)
    else:
        task_id = json.loads(base.put(
            '/rest/fileservice/v1/filesystems/' + fs_id,
            body)[1])['task_id']
        print(common.check_task(base.task_request, task_id))


@log("create todo items")
def create_to_do_items_request_func(body):
    return base.post("/rest/djbaseomwebsite/v1/todo-items", body)


if __name__ == '__main__':
    try:
        main()
    except ScriptException:
        print({})
