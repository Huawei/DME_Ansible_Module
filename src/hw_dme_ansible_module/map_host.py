#!/usr/bin/python
from ansible.module_utils.basic import AnsibleModule
from hw_dme_ansible_core.ansible_base import ARGUMENT_SPEC_BASE
from hw_dme_ansible_core import constants
from hw_dme_ansible_core.ansible_base import AnsibleBase
from hw_dme_ansible_core.common import ScriptException
from hw_dme_ansible_core.volume import map_host

DOCUMENTATION = r'''
---
module: map_host
description:
  - LUN mapping host
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
  volume_wwns:
      description:
          - Indicates the LUN WWN list. A maximum of 100 WWNs are supported.
          - Parameter length of each WWN: 1 to 64.
      type: str
      required: true
  host_id:
      description:
          - Host ID.
          - Parameter length: 1 to 64.
      type: str
      required: true
  storage_id:
      description:
          - Mapping policy – ID of the storage device.
          - Parameter length: 1 to 64.
      type: str
      required: false
  start_host_lun_id:
      description:
          - Mapping policy – Start host LUN ID.
      type: str
      required: false
  auto_zoning:
      description:
          - Mapping policy – Enabling or disabling of automatic zone creation.
          - If the parameter does not exist or is set to false, a zone is not
          - created.
      type: str
      required: false
  zone_policy_id:
      description:
          - Mapping policy – Zone policy. If this parameter is not specified,
          - the default zone policy is used to create a zone.
          - Parameter length: 1 to 64.
      type: str
      required: false
  target_fcports:
      description:
          - Mapping policy – Port WWN list.
          - Parameter length: 1 to 63.
      type: str
      required: false
  target_fcportgroups:
      description:
          - Mapping policy – Port group ID list.
          - Parameter length: 1 to 63.
      type: str
      required: false
  mapping_view_id:
      description:
          - Mapping view – ID of the mapping view on the device.
          - Parameter length: 1 to 31.
      type: str
      required: false
  mapping_view_name:
      description:
          - Mapping view – Name of the mapping view on the device.
          - Parameter length: 1 to 255
          - Constraint: The value can contain only letters, digits, periods (.),
          - underscores (_), and hyphens (-).For the OceanStor Dorado 6.1.0
          - storage system and systems of later versions, the value contains
          - 1 to 255 bytes. In other scenarios,the value contains 1 to 31 bytes.
      type: str
      required: false
  lun_group_id:
      description:
          - Mapping view – ID of the LUN group on the device.
          - Parameter length: 1 to 31.
      type: str
      required: false
  lun_group_name:
      description:
          - Mapping view – Name of the LUN group on the device.
          - Parameter length: 1 to 255.
      type: str
      required: false
  port_group_id:
      description:
          - Mapping view – ID of the port group on the device.
          - Parameter length: 1 to 31.
      type: str
      required: false
'''


def run_module(params, ansible_base, module):
    def map_host_request_func(param):
        return ansible_base.post(constants.MAP_HOST_URL, param)

    result = {}

    try:
        result['data'] = map_host(params,
                                  map_host_request_func,
                                  ansible_base.task_request,
                                  ansible_base.lun_id_convert_func)
        result['msg'] = 'LUN is successfully mapped to host.'
    except ScriptException as ex:
        result['msg'] = 'LUN fails to be mapped to host. Fault cause: %s' % ex
        result['failed'] = True
    module.exit_json(**result)


def main():
    argument_spec = dict(
        volume_wwns=dict(required=True, type='str'),
        host_id=dict(required=True, type='str'),
        storage_id=dict(required=False, type='str'),
        start_host_lun_id=dict(required=False, type='str'),
        auto_zoning=dict(required=False, type='str'),
        zone_policy_id=dict(required=False, type='str'),
        target_fcports=dict(required=False, type='str'),
        target_fcportgroups=dict(required=False, type='str'),
        mapping_view_id=dict(required=False, type='str'),
        mapping_view_name=dict(required=False, type='str'),
        lun_group_id=dict(required=False, type='str'),
        lun_group_name=dict(required=False, type='str'),
        port_group_id=dict(required=False, type='str')
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
