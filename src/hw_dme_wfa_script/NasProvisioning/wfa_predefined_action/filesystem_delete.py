# -*- coding: utf-8
import json
from wfa_predefined_action import base
import datetime
from base import log
from hw_dme_ansible_core import common


@log("get filesystem")
def get_file_system_request_func(param):
    return base.get(
        "/rest/fileservice/v1/filesystems/" + param)


@log("get nfs share")
def get_nfs_share_request_func(param):
    body = {"page_no": 1, "page_size": 100,
            "fs_id": param.get("fs_id")}
    return base.post(
        "/rest/fileservice/v1/nfs-shares/query", body)


@log("get cifs share")
def get_cifs_share_request_func(param):
    body = {"page_no": 1, "page_size": 100,
            "fs_id": param.get("fs_id")}
    return base.post(
        "/rest/fileservice/v1/cifs-shares/query", body)


@log("delete nfs share")
def delete_nfs_share_request_func(body):
    return base.post("/rest/fileservice/v1/nfs-shares/delete", body)


@log("delete cifs share")
def delete_cifs_share_request_func(body):
    return base.post("/rest/fileservice/v1/cifs-shares/delete", body)


@log("delete filesystem")
def delete_file_system_request_func(body):
    return base.post("/rest/fileservice/v1/filesystems/delete", body)


@log("create todo group")
def create_to_do_group_request_func(body):
    return base.post("/rest/djbaseomwebsite/v1/todo-groups", body)


@log("get todo group")
def get_to_do_group_request_func(param):
    return base.get(
        "/rest/djbaseomwebsite/v1/todo-groups?limit=20&start=0&group_id=" + param)


@log("create todo items")
def create_to_do_items_request_func(body):
    return base.post("/rest/djbaseomwebsite/v1/todo-items", body)


def delete_to_do_nfs(param, fs_info, todo_group_info):
    # 查询nfs详情
    response = get_nfs_share_request_func(param)
    nfs_share_list = json.loads(response).get("nfs_share_info_list")

    # 构建删除nfs共享请求体
    nfs_share_ids, nfs_detail = build_body(nfs_share_list)

    request_body_param = {"nfs_share_ids": nfs_share_ids,
                          "nfs_detail": nfs_detail}
    request_body = json.JSONEncoder().encode(request_body_param)
    body = {"name": "delete_nfs_from_" +
                    datetime.datetime.now().strftime('%Y%m%d%H%M%S'),
            "description": "",
            "group_id": todo_group_info.get("id"),
            "request_body": request_body,
            "request_method": "POST",
            "request_uri": "/rest/dmefilewebsite/v1/nfs-shares/delete",
            "service_type": "delete_nfs_share"}
    create_to_do_items_request_func(body)


def delete_to_do_cifs(param, fs_info, todo_group_info):
    # 查询nfs详情
    response = get_cifs_share_request_func(param)
    cifs_share_list = json.loads(response).get(
        "cifs_shares")

    # 构建删除cifs共享请求体
    cifs_share_ids, cifs_detail = build_body(cifs_share_list)

    request_body_param = {"cifs_share_ids": cifs_share_ids,
                          "cifs_datails": cifs_detail}
    request_body = json.JSONEncoder().encode(request_body_param)
    body = {"name": "delete_cifs_from_" +
                    datetime.datetime.now().strftime('%Y%m%d%H%M%S'),
            "description": "",
            "group_id": todo_group_info.get("id"),
            "request_body": request_body,
            "request_method": "POST",
            "request_uri": "/rest/dmefilewebsite/v1/cifs-shares/delete",
            "service_type": "delete_cifs_share"}
    create_to_do_items_request_func(body)


def delete_to_do_file_system(fs_info, todo_group_info):
    response = get_to_do_group_request_func(todo_group_info.get("id"))
    todo_groups = json.loads(response).get("todo_groups")

    item_list = todo_groups[0].get("item_list")

    request_body_param = {
        "file_system_ids": [fs_info.get("id")],
        "file_system_detail": [{"name": fs_info.get("name"),
                                "storage_name": fs_info.get("storage_name"),
                                "fs_raw_id": fs_info.get("fs_raw_id"),
                                "capacity": fs_info.get("capacity")}]}
    request_body = json.JSONEncoder().encode(request_body_param)
    body = {"name": "delete_" +
                    datetime.datetime.now().strftime('%Y%m%d%H%M%S'),
            "description": "",
            "group_id": todo_group_info.get("id"),
            "request_body": request_body,
            "request_method": "POST",
            "request_uri": "/rest/dmefilewebsite/v1/filesystems/delete",
            "service_type": "delete_filesystem"}
    if item_list:
        depend_ids = []
        for item in item_list:
            depend_ids.append(item.get("id"))
        body["depend_ids"] = depend_ids
    create_to_do_items_request_func(body)


def main():
    # 获取命令参数，入参为该业务必须的参数字段
    param = base.get_param()
    base.init_client(param)
    # 根据业务，通过client 请求，并组装参数返回
    # 查询文件系统详情
    response = get_file_system_request_func(param.get("fs_id"))
    fs_info = json.loads(response)
    if param.get("todo") == "true":
        # 创建待办任务组
        body = {"name": "todo_delete_" +
                        datetime.datetime.now().strftime('%Y%m%d%H%M%S'),
                "description": "", "skip_fail_item": False}
        response = create_to_do_group_request_func(body)
        todo_group_info = json.loads(response)

        # 有nfs则添加删除nfs待办进待办组
        if fs_info.get("nfs_count") > 0:
            delete_to_do_nfs(param, fs_info, todo_group_info)

        # 有cifs则添加删除nfs待办进待办组
        if fs_info.get("cifs_count") > 0:
            delete_to_do_cifs(param, fs_info, todo_group_info)

        # 删除文件系统加入待办组
        delete_to_do_file_system(fs_info, todo_group_info)
    else:
        if fs_info.get("nfs_count") > 0:
            # 查询nfs详情
            response = get_nfs_share_request_func(param)
            nfs_share_list = json.loads(response).get(
                "nfs_share_info_list")

            # 构建删除nfs共享请求体
            nfs_share_ids = build_request_body(nfs_share_list)
            request_body = {"nfs_share_ids": nfs_share_ids}
            response = delete_nfs_share_request_func(request_body)
            task_id = json.loads(response)['task_id']
            common.check_task(base.task_request, task_id)

        if fs_info.get("cifs_count") > 0:
            # 查询cifs详情
            response = get_cifs_share_request_func(param)
            cifs_share_list = json.loads(response).get(
                "cifs_share_info_list")

            # 构建删除cifs共享请求体
            cifs_share_ids = build_request_body(cifs_share_list)
            request_body = {"cifs_share_ids": cifs_share_ids}
            response = delete_cifs_share_request_func(request_body)
            task_id = json.loads(response)['task_id']
            common.check_task(base.task_request, task_id)

        request_body = {"file_system_ids": [param.get("fs_id")]}
        response = delete_file_system_request_func(request_body)
        task_id = json.loads(response)['task_id']
        common.check_task(base.task_request, task_id)


def build_body(share_list):
    share_ids = []
    share_detail = []
    for item in share_list:
        share_ids.append(item.get("id"))
        share_detail.append({"name": item.get("name"),
                             "share_path": item.get("share_path")})
    return share_ids, share_detail


def build_request_body(share_list):
    share_ids = []
    for item in share_list:
        share_ids.append(item.get("id"))
    return share_ids


if __name__ == "__main__":
    main()
