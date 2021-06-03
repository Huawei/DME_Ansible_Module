# -*- coding: utf-8 -*
import json
from hw_dme_ansible_core.common import check_empty_param
from hw_dme_ansible_core.common import check_task
from hw_dme_ansible_core.common import volume_id_conversion
from hw_dme_ansible_core.common import volume_ids_conversion
from hw_dme_ansible_core.common import del_none_key
from hw_dme_ansible_core.common import build_body


def query(param, query_luns_request_func):
    param = del_none_key(param)
    body = {}
    if param:
        keys = ('limit', 'offset', 'sort_dir', 'sort_key', 'name', 'status',
                'service_level_id', 'volume_wwn', 'storage_id', 'pool_raw_id',
                'host_id', 'hostgroup_id', 'unmapped_host_id',
                'unmapped_hostgroup_id', 'project_id', 'allocate_type',
                'attached', 'query_mode', 'protected', 'pg_id')
        body = build_body(keys, param)
    return query_luns_request_func(body)


def delete(param, delete_luns_request_func, task_request, lun_id_convert_func):
    check_empty_param(param, 'volume_wwns')
    lun_ids = volume_ids_conversion(param.get('volume_wwns'),
                                    lun_id_convert_func)
    body = {'volume_ids': lun_ids}
    task_id = json.loads(delete_luns_request_func(body))['task_id']
    return check_task(task_request, task_id)


def modify(param, modify_luns_request_func, task_request,
           volume_id_conversion_request_fun):
    check_empty_param(param, 'volume_wwn')
    param = del_none_key(param)
    volume_id = volume_id_conversion(param.get('volume_wwn'),
                                     volume_id_conversion_request_fun)
    body = build_modify_param(param)
    task_id = json.loads(modify_luns_request_func(volume_id, body))['task_id']
    return check_task(task_request, task_id)


def build_modify_param(param):
    body = {
        "volume": {
            "name": param.get('name'),
            "description": param.get('description'),
            "owner_controller": param.get('owner_controller'),
            "prefetch_policy": param.get('prefetch_policy'),
            "prefetch_value": param.get('prefetch_value'),
            "tuning": {
                "smarttier": param.get('smarttier'),
                "smartqos": {
                    "maxbandwidth": param.get('maxbandwidth'),
                    "maxiops": param.get('maxiops'),
                    "minbandwidth": param.get('minbandwidth'),
                    "miniops": param.get('miniops'),
                    "control_policy": param.get('control_policy'),
                    "latency": param.get('latency'),
                    "enabled": param.get('qos_enabled'),
                }
            }
        }
    }
    return body


def map_host(param, map_host_request, check_task_request, lun_id_convert_func):
    check_empty_param(param, 'volume_wwns', 'host_id')
    body = {'volume_ids': volume_ids_conversion(param.get('volume_wwns'),
                                                lun_id_convert_func),
            'host_id': param.get('host_id')}
    if param.get('storage_id') or param.get('start_host_lun_id'):
        body['mapping_policy'] = get_mapping_policy(param)
    task_id = json.loads(map_host_request(body))['task_id']
    return check_task(check_task_request, task_id)


def map_hostgroup(param, map_hostgroup_request, check_task_request,
                  lun_id_convert_func):
    check_empty_param(param, 'volume_wwns', 'hostgroup_id')
    body = {'volume_ids': volume_ids_conversion(param.get('volume_wwns'),
                                                lun_id_convert_func),
            'hostgroup_id': param.get('hostgroup_id')}
    if param.get('storage_id') or param.get('start_host_lun_id'):
        body['mapping_policy'] = get_mapping_policy(param)
    task_id = json.loads(map_hostgroup_request(body))['task_id']
    return check_task(check_task_request, task_id)


def get_mapping_policy(param):
    mapping_policy = build_mapping_policy(param)
    if param.get('mapping_view_id') or param.get('mapping_view_name'):
        mapping_view = build_mapping_view(param)
        mapping_policy['mapping_view'] = mapping_view

    return mapping_policy


def build_mapping_policy(param):
    mapping_policy_keys = ('storage_id', 'start_host_lun_id', 'auto_zoning',
                           'zone_policy_id')
    mapping_policy = build_body(mapping_policy_keys, param)

    if param.get('target_fcports'):
        mapping_policy['target_fcports'] = param.get(
            'target_fcports').split(',')
    if param.get('target_fcportgroups'):
        mapping_policy['target_fcportgroups'] = param.get(
            'target_fcportgroups').split(',')
    return mapping_policy


def build_mapping_view(param):
    mapping_view_keys = ('mapping_view_id', 'mapping_view_name',
                         'lun_group_id', 'lun_group_name', 'port_group_id')
    return build_body(mapping_view_keys, param)


def unmap_host(param, unmap_host_request, check_task_request,
               lun_id_convert_func):
    check_empty_param(param, 'volume_wwns', 'host_id')
    body = {'volume_ids': volume_ids_conversion(param.get('volume_wwns'),
                                                lun_id_convert_func),
            'host_id': param.get('host_id')}
    task_id = json.loads(unmap_host_request(body))['task_id']
    return check_task(check_task_request, task_id)


def unmap_hostgroup(param, unmap_hostgroup_request, check_task_request,
                    lun_id_convert_func):
    check_empty_param(param, 'volume_wwns', 'hostgroup_id')
    body = {'volume_ids': volume_ids_conversion(param.get('volume_wwns'),
                                                lun_id_convert_func),
            'hostgroup_id': param.get('hostgroup_id')}
    task_id = json.loads(unmap_hostgroup_request(body))['task_id']
    return check_task(check_task_request, task_id)


def lun_add_to_service_level(param, lun_update_service_level_request,
                             check_task_request, lun_id_convert_func):
    check_empty_param(param, 'service_level_id', 'volume_wwns')
    body = {'volume_ids': volume_ids_conversion(param.get('volume_wwns'),
                                                lun_id_convert_func),
            'service_level_id': param.get('service_level_id')}
    if param.get('attributes_auto_change'):
        body['attributes_auto_change'] = param.get('attributes_auto_change')
    task_id = json.loads(lun_update_service_level_request(body))['task_id']
    return check_task(check_task_request, task_id)


def lun_remove_service_level(param, lun_remove_service_level_request,
                             check_task_request, lun_id_convert_func):
    check_empty_param(param, 'volume_wwns')
    body = {'volume_ids': volume_ids_conversion(param.get('volume_wwns'),
                                                lun_id_convert_func)}
    task_id = json.loads(lun_remove_service_level_request(body))['task_id']
    return check_task(check_task_request, task_id)


def lun_update_service_level(param, lun_update_service_level_request,
                             check_task_request, lun_id_convert_func):
    check_empty_param(param, 'service_level_id', 'volume_wwns')
    body = {'volume_ids': volume_ids_conversion(param.get('volume_wwns'),
                                                lun_id_convert_func),
            'service_level_id': param.get('service_level_id')}
    if param.get('attributes_auto_change'):
        body['attributes_auto_change'] = param.get('attributes_auto_change')
    task_id = json.loads(lun_update_service_level_request(body))['task_id']
    return check_task(check_task_request, task_id)


def customize_volumes(param, customize_volumes_func, check_task_request):
    check_empty_param(param, 'storage_id', 'pool_id', 'name', 'count',
                      'capacity')
    param = del_none_key(param)

    keys = ('storage_id', 'pool_id', 'owner_controller',
            'initial_distribute_policy', 'prefetch_policy', 'prefetch_value')
    volumes = ('name', 'start_lun_id', 'capacity', 'count', 'start_suffix')
    tunings = ('smart_tier', 'deduplication_enabled', 'compression_enabled',
               'alloction_type', 'workload_type_raw_id')
    smart_qoss = ('max_bandwidth', 'max_iops', 'min_bandwidth', 'min_iops',
                  'latency')
    mappings = ('host_id', 'hostgroup_id', 'start_host_lun_id')
    mapping_views = ('mapping_view_raw_id', 'mapping_view_name',
                     'lun_group_raw_id', 'lun_group_name', 'port_group_raw_id')

    body = build_body(keys, param)
    body['lun_specs'] = [build_body(volumes, param)]

    if build_body(tunings, param):
        body['tuning'] = build_body(tunings, param)
    if build_body(smart_qoss, param):
        body['tuning']['smart_qos'] = build_body(smart_qoss, param)
    if build_body(mappings, param):
        body['mapping'] = build_body(mappings, param)
    if build_body(mapping_views, param):
        body['mapping']['mapping_view'] = build_body(mapping_views, param)

    task_id = json.loads(customize_volumes_func(body))['task_id']
    return check_task(check_task_request, task_id)


def create_volumes(param, create_volumes_func, check_task_request,
                   lun_id_convert_func):
    check_empty_param(param, 'service_level_id', 'name', 'capacity', 'count')
    keys = ('service_level_id', 'project_id', 'availability_zone')
    volume = ('name', 'description', 'capacity', 'count', 'start_suffix')

    body = build_body(keys, param)

    body['volumes'] = [build_body(volume, param)]

    if param.get('host_id') or param.get('hostgroup_id'):
        body['mapping'] = {'host_id': param.get('host_id'),
                           'hostgroup_id': param.get('hostgroup_id')}
    if param.get('affinity') == 'true':
        affinity_volume = volume_id_conversion(param.get('affinity_volume'),
                                               lun_id_convert_func)
        body['scheduler_hints'] = {'affinity': param.get('affinity'),
                                   'affinity_volume': affinity_volume}

    task_id = json.loads(create_volumes_func(body))['task_id']
    return check_task(check_task_request, task_id)
