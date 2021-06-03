# -*- coding: utf-8 -*
from hw_dme_ansible_core.common import list_param_conversion
from hw_dme_ansible_core.common import ScriptException
from hw_dme_ansible_core.common import check_empty_param
from hw_dme_ansible_core.common import del_none_key
from hw_dme_ansible_core.common import build_body


def add(param, add_host_request_func):
    check_empty_param(param, 'type', 'access_mode')
    param = del_none_key(param)
    check_empty_param(param, 'host_name')
    # 转换启动参数
    keys = ('access_mode', 'type', 'host_name', 'description',
            'azs', 'project_id', 'sync_to_storage', 'multipath_type',
            'path_type', 'failover_mode', 'special_mode_type')
    body = build_body(keys, param)

    body['initiator'] = initiator_conversion(param)
    list_param_conversion(body, 'azs')
    return add_host_request_func(body)


def delete(param, delete_host_request_func):
    check_empty_param(param, 'host_id')
    host_id = param.get('host_id')
    request_param = None
    if param.get('sync_to_storage'):
        request_param = {'sync_to_storage': param['sync_to_storage']}
    return delete_host_request_func(host_id, request_param)


def update_general(param, update_host_request):
    check_empty_param(param, 'host_id')
    host_id = param.get('host_id')
    param = del_none_key(param)
    keys = ('ip', 'host_name', 'os_type', 'azs', 'project_id')
    body = build_body(keys, param)

    list_param_conversion(body, 'azs')
    return update_host_request(host_id, body)


def update_accessinfo(param, update_host_request):
    check_empty_param(param, 'host_id')
    host_id = param.get('host_id')
    param = del_none_key(param)
    keys = ('ip', 'port', 'host_name', 'description', 'os_type', 'azs', 'project_id',
            'sync_to_storage', 'multipath_type', 'path_type', 'failover_mode', 'special_mode_type')
    body = build_body(keys, param)

    list_param_conversion(body, 'azs')
    return update_host_request(host_id, body)


def query(param, query_host_request_func):
    body = {}
    if param:
        keys = ('limit', 'start', 'name', 'sort_key', 'sort_dir', 'host_group_name', 'ip',
                'display_status', 'managed_status', 'os_type', 'access_mode', 'az_id', 'az_ids', 'project_id')
        body = build_body(keys, param)

    list_param_conversion(body, 'managed_status', 'az_ids')
    return query_host_request_func(body)


def initiator_conversion(param):
    ISCSI_initiator = param.get('iSCSI_initiator')
    FC_initiator = param.get('FC_initiator')
    # 检验启动参数是否为空
    if param.get('iSCSI_initiator') is None and param.get('FC_initiator') is None:
        raise ScriptException('initiator cannot be empty.')
    initiator = []
    if ISCSI_initiator:
        initiator += [{'protocol': 'ISCSI', 'port_name': i} for i in ISCSI_initiator.split(',')]
    if FC_initiator:
        initiator += [{'protocol': 'FC', 'port_name': i} for i in FC_initiator.split(',')]
    return initiator
