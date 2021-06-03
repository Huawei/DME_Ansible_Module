#!/usr/bin/python
from hw_dme_ansible_core.volume import customize_volumes
from hw_dme_ansible_core.ansible_base import AnsibleBase
from hw_dme_ansible_core.common import ScriptException
from hw_dme_ansible_core import constants
from ansible.module_utils.basic import AnsibleModule
from hw_dme_ansible_core.ansible_base import ARGUMENT_SPEC_BASE

DOCUMENTATION = r'''
---
module: lun_customize_create
description:
  - Create customized LUNs
Options:
  dme_ip:
    description:
      - DME IP.
    type: str
    required: true
  dme_port:
    description:
      - Northbond api port, default: 26335
    type: str
    required: false
  dme_user:
    description:
      - Northbond api username.
    type: str
    required: true
  dme_password:
    description:
      - Northbond api password.
    type: str
    required: true
  dme_certificate_path:
    description:
      - DME certificate path.
    type: str
    required: false
  storage_id:
    description:
      - Storage device ID.
      - Parameter length: 1 to 64.
    type: str
    required: true
  pool_id:
    description:
      - Storage pool ID.
      - Parameter length: 1 to 64.
    type: str
    required: true
  name:
    description:
      - LUN name.
      - Parameter length: 1 to 255.
    type: str
    required: true
  capacity:
    description:
      - LUN capacity.
      - Parameter length: 1 to 262144.
    type: str
    required: true
  count:
    description:
      - Number of LUNs.
      - Parameter length: 1 to 500.
    type: str
    required: true
  owner_controller:
    description:
      - Owning controller.
      - Parameter length: 1 to 64.
    type: str
    required: false
  initial_distribute_policy:
    description:
      - Initial capacity allocation policy.
      - Value range:
        - 0 (automatic)
        - 1 (highest_performance)
        - 2 (performance)
        - 3 (capacity)
    type: str
    required: false
  prefetch_policy:
    description:
      - Prefetch policy.
      - Value range:
        - 0 (no_prefetch)
        - 1 (constant_prefetch)
        - 2 (variable_prefetch)
        - 3 (intelligent_prefetch)
    type: str
    required: false
  prefetch_value:
    description:
      - Prefetch policy value.
      - Parameter length: 1 to 1024.
    type: str
    required: false
  hostgroup_id:
    description:
      - Mapping – Host group ID.
      - Parameter length: 1 to 64.
    type: str
    required: false
  host_id:
    description:
      - Mapping – Host ID.
      - Parameter length: 1 to 64.
    type: str
    required: false
  start_lun_id:
    description:
      - Start LUN ID.
      - Parameter length: 1 to 64.
    type: str
    required: false
  start_suffix:
    description:
      - Start suffix number of a LUN.
      - Parameter length: 1 to 64.
    type: str
    required: false
  smart_tier:
    description:
      - Data relocation policy.
      - Value range:
        - 0 (no_migration)
        - 1 (automatic_migration)
        - 2 (migration_to_higher)
        - 3 (migration_to_lower)
    type: str
    required: false
  deduplication_enabled:
    description:
      - Deduplication.
    type: str
    required: false
  compression_enabled:
    description:
      - Data compression.
    type: str
    required: false
  alloction_type:
    description:
      - LUN allocation type.
      - Value range:
        - thin
        - thick
    type: str
    required: false
  workload_type_raw_id:
    description:
      - Application type ID. The value is obtained from a storage device.
      - Parameter length: 1 to 64.
    type: str
    required: false
  max_bandwidth:
    description:
      - QoS attribute – Max. bandwidth.
    type: str
    required: false
  max_iops:
    description:
      -  QoS attribute – Max. IOPS.
    type: str
    required: false
  min_bandwidth:
    description:
      - QoS attribute – Min. bandwidth.
    type: str
    required: false
  min_iops:
    description:
      - QoS attribute – Min. IOPS.
    type: str
    required: false
  latency:
    description:
      - QoS attribute – Latency.
    type: str
    required: false
  start_host_lun_id:
    description:
      - Mapping – Start host LUN ID of the mapped LUN.
      - Parameter length: 1 to 64.
    type: str
    required: false
  mapping_view_raw_id:
    description:
      - Mapping view – ID of the mapping view on the device.
      - Parameter length: 1 to 64.
    type: str
    required: false
  mapping_view_name:
    description:
      - Mapping view – Name of the mapping view on the device.
      - Parameter length: 1 to 255.
    type: str
    required: false
  lun_group_raw_id:
    description:
      - Mapping view – ID of the LUN group on the device.
      - Parameter length: 1 to 64.
    type: str
    required: false
  lun_group_name:
    description:
      - Mapping view – Name of the LUN group on the device.
      - Parameter length: 1 to 255.
    type: str
    required: false
  port_group_raw_id:
    description:
      - Mapping view – ID of the port group on the device.
      - Parameter length: 1 to 64.
    type: str
    required: false
'''


def run_module(params, ansible_base, module):
    def customize_luns_request_func(param):
        return ansible_base.post(constants.LUN_CUSTOMIZE_URL, param)

    result = {}

    try:
        result['data'] = customize_volumes(params, customize_luns_request_func,
                                           ansible_base.task_request)
        result['msg'] = 'LUN is successfully created.'
    except ScriptException as ex:
        result['msg'] = 'LUN fails to be created. Fault cause: %s.' % ex
        result['failed'] = True
    module.exit_json(**result)


def main():
    argument_spec = dict(
        storage_id=dict(required=True, type='str'),
        pool_id=dict(required=True, type='str'),
        name=dict(required=True, type='str'),
        capacity=dict(required=True, type='str'),
        count=dict(required=True, type='str'),
        owner_controller=dict(required=False, type='str'),
        initial_distribute_policy=dict(required=False, type='str'),
        prefetch_policy=dict(required=False, type='str'),
        prefetch_value=dict(required=False, type='str'),
        hostgroup_id=dict(required=False, type='str'),
        host_id=dict(required=False, type='str'),
        start_lun_id=dict(required=False, type='str'),
        start_suffix=dict(required=False, type='str'),
        smart_tier=dict(required=False, type='str'),
        deduplication_enabled=dict(required=False, type='str'),
        compression_enabled=dict(required=False, type='str'),
        alloction_type=dict(required=False, type='str'),
        workload_type_raw_id=dict(required=False, type='str'),
        max_bandwidth=dict(required=False, type='str'),
        max_iops=dict(required=False, type='str'),
        min_bandwidth=dict(required=False, type='str'),
        min_iops=dict(required=False, type='str'),
        latency=dict(required=False, type='str'),
        start_host_lun_id=dict(required=False, type='str'),
        mapping_view_raw_id=dict(required=False, type='str'),
        mapping_view_name=dict(required=False, type='str'),
        lun_group_raw_id=dict(required=False, type='str'),
        lun_group_name=dict(required=False, type='str'),
        port_group_raw_id=dict(required=False, type='str')
    )

    argument_spec.update(ARGUMENT_SPEC_BASE)
    module = AnsibleModule(
        argument_spec=argument_spec
    )
    params = module.params
    ansible_base = AnsibleBase(params['dme_ip'],
                               params['dme_port'],
                               params['dme_user'],
                               params['dme_password'],
                               params['dme_certificate_path'])
    run_module(params, ansible_base, module)


if __name__ == '__main__':
    main()
