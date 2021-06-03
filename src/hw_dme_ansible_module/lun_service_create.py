#!/usr/bin/python
from hw_dme_ansible_core.volume import create_volumes
from hw_dme_ansible_core.ansible_base import AnsibleBase
from hw_dme_ansible_core.common import ScriptException
from hw_dme_ansible_core import constants
from ansible.module_utils.basic import AnsibleModule
from hw_dme_ansible_core.ansible_base import ARGUMENT_SPEC_BASE

DOCUMENTATION = r'''
---
module: lun_service_create
description:
 - Create LUNs based on a service level
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
  service_level_id:
    description:
      - Service level ID.
      - Parameter length: 1 to 64.
    type: str
    required: true
  project_id:
    description:
      - Project ID.
      - Parameter length: 1 to 64.
    type: str
    required: false
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
  availability_zone:
    description:
      - AZ ID.
      - Parameter length: 1 to 64.
    type: str
    required: false
  description:
    description:
      - Description.
      - Parameter length: 1 to 255.
    type: str
    required: false
  start_suffix:
    description:
      - Start suffix number of a LUN.
      - Parameter length: 1 to 255.
    type: str
    required: false
  affinity_volume:
    description:
      - WWN of the LUN for which affinity is set.
      - Parameter length: 1 to 64.
    type: str
    required: false
  affinity:
    description:
      - Enabling affinity.
    type: str
    required: false
  hostgroup_id:
    description:
      - Host group ID.
      - Parameter length: 1 to 64.
    type: str
    required: false
  host_id:
    description:
      - Host ID.
      - Parameter length: 1 to 64.
    type: str
    required: false
'''


def run_module(params, ansible_base, module):
    def create_luns_request_func(param):
        return ansible_base.post(constants.LUN_CREATE_URL, param)

    result = {}

    try:
        result['data'] = create_volumes(params, create_luns_request_func,
                                        ansible_base.task_request,
                                        ansible_base.lun_id_convert_func)
        result['msg'] = 'LUN is successfully created.'
    except ScriptException as ex:
        result['msg'] = 'LUN fails to be created. Fault cause: %s.' % ex
        result['failed'] = True
    module.exit_json(**result)


def main():
    argument_spec = dict(
        service_level_id=dict(required=True, type='str'),
        name=dict(required=True, type='str'),
        capacity=dict(required=True, type='str'),
        count=dict(required=True, type='str'),
        project_id=dict(required=False, type='str'),
        availability_zone=dict(required=False, type='str'),
        description=dict(required=False, type='str'),
        start_suffix=dict(required=False, type='str'),
        hostgroup_id=dict(required=False, type='str'),
        host_id=dict(required=False, type='str'),
        affinity_volume=dict(required=False, type='str'),
        affinity=dict(required=False, type='str')
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
