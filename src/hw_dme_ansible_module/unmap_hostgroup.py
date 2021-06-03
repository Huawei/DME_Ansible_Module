#!/usr/bin/python
from ansible.module_utils.basic import AnsibleModule
from hw_dme_ansible_core.ansible_base import ARGUMENT_SPEC_BASE
from hw_dme_ansible_core import constants
from hw_dme_ansible_core.ansible_base import AnsibleBase
from hw_dme_ansible_core.common import ScriptException
from hw_dme_ansible_core.volume import unmap_hostgroup

DOCUMENTATION = r'''
---
module: unmap_hostgroup
description:
  - LUN Unmapping host group
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
  hostgroup_id:
      description:
          - Host group ID.
          - Parameter length: 1 to 64.
      type: str
      required: true
'''


def run_module(params, ansible_base, module):
    def unmap_hostgroup_request_func(param):
        return ansible_base.post(constants.UNMAP_HOSTGROUP_URL, param)

    result = {}

    try:
        result['data'] = unmap_hostgroup(params,
                                         unmap_hostgroup_request_func,
                                         ansible_base.task_request,
                                         ansible_base.lun_id_convert_func)
        result['msg'] = 'LUN is successfully unmapped from host group.'
    except ScriptException as ex:
        result[
            'msg'] = 'LUN fails to be unmapped from host group. Fault cause: %s' % ex
        result['failed'] = True
    module.exit_json(**result)


def main():
    argument_spec = dict(
        volume_wwns=dict(required=True, type='str'),
        hostgroup_id=dict(required=True, type='str')
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
