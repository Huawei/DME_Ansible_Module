# -*- coding: utf-8 -*
from hw_dme_ansible_core.common import list_param_conversion
from hw_dme_ansible_core.common import check_empty_param
from hw_dme_ansible_core.common import build_body


def add(param, add_host_group_request_func):
    check_empty_param(param, 'name', 'host_ids')
    keys = ('name', 'host_ids', 'azs', 'project_id', 'description')
    body = build_body(keys, param)
    list_param_conversion(body, 'host_ids', 'azs')
    return add_host_group_request_func(body)


def delete(param, delete_host_group_request_func):
    check_empty_param(param, 'hostgroup_id')
    hostgroup_id = param.get('hostgroup_id')
    body = None
    if param.get('sync_to_storage'):
        body = {'sync_to_storage': param['sync_to_storage']}
    return delete_host_group_request_func(hostgroup_id, body)


def update(param, update_host_group_request_func):
    check_empty_param(param, 'hostgroup_id', 'name')
    hostgroup_id = param.get('hostgroup_id')
    keys = ('project_id', 'name', 'description', 'azs')
    body = build_body(keys, param)
    list_param_conversion(body, 'azs')
    return update_host_group_request_func(hostgroup_id, body)


def query(param, query_host_group_request_func):
    body = {}
    if param:
        keys = ('limit', 'start', 'sort_dir', 'sort_key', 'name', 'project_id',
                'az_ids', 'managed_status')
        body = build_body(keys, param)
    list_param_conversion(body, 'managed_status', 'az_ids')
    return query_host_group_request_func(body)


def add_or_remove_host(param, add_or_remove_host_from_group_request_func):
    check_empty_param(param, 'hostgroup_id', 'host_ids')
    list_param_conversion(param, 'host_ids')
    hostgroup_id = param.get('hostgroup_id')
    host_ids = param.get('host_ids')
    request_param = {'host_ids': host_ids,
                     'sync_to_storage': param.get('sync_to_storage', False)}
    return add_or_remove_host_from_group_request_func(hostgroup_id,
                                                      request_param)
