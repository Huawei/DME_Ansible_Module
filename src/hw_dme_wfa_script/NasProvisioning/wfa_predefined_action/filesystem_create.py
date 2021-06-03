# -*- coding: utf-8
import datetime
import json
import sys

from hw_dme_ansible_core import common
from hw_dme_ansible_core import param_base
from hw_dme_ansible_core.common import ScriptException
from wfa_predefined_action import base


def main():
    try:
        param = base.get_param()
        base.init_client(param)
        if param.get('units') == 'TB':
            param['capacity'] = int(param['capacity']) * 1024
        if param.get('todo') == 'true':
            print('Start to create file system to-do.')
        else:
            print('Start to create file system.')
        storage_info = get_storage_info(base, param['storage_id'])
        response = build_and_send(param,
                                  param_base.is_dorado_device(storage_info))
        if response[0] == 200:
            print('File system to-do is successfully created.')
        elif response[0] == 202:
            task_id = json.loads(response[1])['task_id']
            common.check_task(base.task_request, task_id)
            print('File system is successfully created.')
        else:
            print('File system fails to be created. Fault cause: %s.' %
                  response[1])
            raise ScriptException()
    except ScriptException as ex:
        print('File system fails to be created. Fault cause: %s.' % ex)
        sys.exit(-1)


def build_and_send(param, is_nas):
    nfs_share_client_addition = []
    build_client_r(nfs_share_client_addition, param)
    build_client_read_write(nfs_share_client_addition, param)

    ips = client_data(param)
    share_view = ''
    for ip in ips:
        share_view = share_view + ip + ':/' + param['name'] + '/;'
    if share_view != '':
        share_view = share_view[:-1] + ''
    create_nfs_share_param = {
        "description": share_view,
        "share_path": "/" + param['name'] + "/",
        "character_encoding": "utf-8",
        "nfs_share_client_addition": nfs_share_client_addition
    }
    if not is_nas:
        create_nfs_share_param['show_snapshot_enable'] = False
    req_param = get_req_param(create_nfs_share_param, param, is_nas)
    return send(param, req_param)


def build_client_r(nfs_share_client_addition, param):
    if param.get('add_client_ips_r'):
        add_client_ips_r = param['add_client_ips_r'].split(',')
        for ip in add_client_ips_r:
            if ip:
                nfs_share_client_addition.append(
                    {"name": ip, "permission": "read-only",
                     "write_mode": "synchronization",
                     "permission_constraint": "no_all_squash",
                     "root_permission_constraint": "no_root_squash",
                     "source_port_verification": "insecure",
                     "startSuffix": 1})


def build_client_read_write(nfs_share_client_addition, param):
    if param.get('add_client_ips_rw'):
        add_client_ips_rw = param['add_client_ips_rw'].split(',')
        for ip in add_client_ips_rw:
            if ip:
                nfs_share_client_addition.append(
                    {"name": ip, "permission": "read/write",
                     "write_mode": "synchronization",
                     "permission_constraint": "no_all_squash",
                     "root_permission_constraint": "no_root_squash",
                     "source_port_verification": "insecure",
                     "startSuffix": 1})


def send(param, req_param):
    body_value = json.JSONEncoder().encode(req_param)
    if param.get('todo') == 'true':
        todobody = {"name": "create_filesystem_" + datetime.datetime.now().strftime(
            '%Y%m%d%H%M%S'),
                    "service_type": "create_filesystem",
                    "request_method": "POST",
                    "request_uri": "/rest/fileservice/v1/filesystems/customize-filesystems",
                    "request_body": body_value}
        return base.post('/rest/taskmgmt/v1/todo-items', todobody)
    else:
        return base.post(
            '/rest/fileservice/v1/filesystems/customize-filesystems',
            req_param)


def get_req_param(create_nfs_share_param, param, is_nas):
    req_param = {"storage_id": param['storage_id'],
                 "pool_raw_id": param['pool_id'], "availability_zone": "",
                 "initial_distribute_policy": "auto",
                 "snapshot_expired_enabled": False,
                 "checksum_enabled": True,
                 "automatic_update_time": False,
                 "snapshot_dir_visible": False,
                 "filesystem_specs": [
                     {"name": param['name'], "capacity": param['capacity'],
                      "count": 1}]}
    if len(create_nfs_share_param) != 0:
        req_param["create_nfs_share_param"] = create_nfs_share_param

    if is_nas:
        req_param["vstore_id"] = get_account(param['storage_id'])
        req_param["security_mode"] = "unix"
        req_param["capacity_threshold"] = 80
        req_param["tuning"] = {
            "workload_type_id": "11"
        }
    else:
        storage_info = get_storage_info(base, param['storage_id'])
        req_param["periodic_snapshots_limit"] = 1
        if param['open_dr'] == 'true':
            req_param["snapshot_reserved_space_percentage"] = param[
                "snapshot_reserved_space_percentage"]
        else:
            req_param["snapshot_reserved_space_percentage"] = 0
        if is_low_than_v3r6c00(storage_info):
            req_param["tuning"] = {
                "allocation_type": "thick"
            }
        else:
            req_param["tuning"] = {
                "allocation_type": "thick",
                "application_scenario": "user_defined",
                "block_size": "4"
            }
    return req_param


def get_account(storage_id):
    req_param = {"page_size": 1000, "page_no": 1, "storage_id": storage_id}
    accounts = json.loads(base.post(
        "/rest/dmefilewebsite/v1/accounts", req_param)[1])['accounts']
    for account in accounts:
        if account.get('name') == 'System_vStore':
            return account.get('id')
    return ''


def get_storage_info(base, storage_id):
    storage_infos = json.loads(base.get(
        "/rest/storagemgmt/v1/storages?start=1&limit=100")[1])['datas']
    for info in storage_infos:
        if storage_id == info['id']:
            return info


def client_data(param):
    ips = []
    if param.get('add_client_ips_rw'):
        add_client_ips_rw = param['add_client_ips_rw'].split(',')
        for ip in add_client_ips_rw:
            if ip:
                ips.append(ip)
    if param.get('add_client_ips_r'):
        add_client_ips_r = param['add_client_ips_r'].split(',')
        for ip in add_client_ips_r:
            if ip:
                ips.append(ip)
    return ips


def is_low_than_v3r6c00(storage_info):
    # 判断是否低于v3r6c00版本，不支持应用场景
    storage_product_version = storage_info.get('version')
    if storage_product_version <= 'V300R006C00':
        return True
    return False


if __name__ == '__main__':
    main()
