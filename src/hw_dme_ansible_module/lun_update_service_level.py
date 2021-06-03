#!/usr/bin/python
from ansible.module_utils.basic import AnsibleModule
from hw_dme_ansible_core.ansible_base import ARGUMENT_SPEC_BASE
from hw_dme_ansible_core import constants
from hw_dme_ansible_core.ansible_base import AnsibleBase
from hw_dme_ansible_core.common import ScriptException
from hw_dme_ansible_core.volume import lun_update_service_level

DOCUMENTATION = r'''
---
module: lun_update_service_level
description:
  - Add a LUN to a service level
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
  service_level_id:
      description:
          - Service level ID.
          - Parameter length: 1 to 64.
      type: str
      required: true
  attributes_auto_change:
      description:
          - Updating LUN properties based on the service level when the LUN is
          - associated with a service level.
      type: str
      required: False
'''


def run_module(params, ansible_base, module):
    def lun_update_service_level_request_func(param):
        return ansible_base.post(constants.LUN_UPDATE_SERVICE_LEVEL_URL, param)

    result = {}

    try:
        result['data'] = lun_update_service_level(params,
                                                  lun_update_service_level_request_func,
                                                  ansible_base.task_request,
                                                  ansible_base.lun_id_convert_func)
        result[
            'msg'] = 'The service level to which LUN belongs is successfully updated.'
    except ScriptException as ex:
        result[
            'msg'] = 'The service level to which LUN belongs fails to be updated. Fault cause: %s' % ex
        result['failed'] = True
    module.exit_json(**result)


def main():
    argument_spec = dict(
        volume_wwns=dict(required=True, type='str'),
        service_level_id=dict(required=True, type='str'),
        attributes_auto_change=dict(required=False, type='str')
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
