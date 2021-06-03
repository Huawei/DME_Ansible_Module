#!/usr/bin/python
from ansible.module_utils.basic import AnsibleModule
from hw_dme_ansible_core.ansible_base import ARGUMENT_SPEC_BASE
from hw_dme_ansible_core import constants
from hw_dme_ansible_core.ansible_base import AnsibleBase
from hw_dme_ansible_core.common import ScriptException
from hw_dme_ansible_core.volume import lun_remove_service_level

DOCUMENTATION = r'''
---
module: lun_remove_service_level
description:
  - Remove a LUN from a service level
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
'''


def run_module(params, ansible_base, module):
    def lun_remove_service_level_request_func(param):
        return ansible_base.post(constants.LUN_REMOVE_SERVICE_LEVEL_URL, param)

    result = {}

    try:
        result['data'] = lun_remove_service_level(params,
                                                  lun_remove_service_level_request_func,
                                                  ansible_base.task_request,
                                                  ansible_base.lun_id_convert_func)
        result['msg'] = 'LUN is successfully removed from service level.'
    except ScriptException as ex:
        result[
            'msg'] = 'LUN fails to be removed from service level. Fault cause: %s' % ex
        result['failed'] = True
    module.exit_json(**result)


def main():
    argument_spec = dict(
        volume_wwns=dict(required=True, type='str')
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
