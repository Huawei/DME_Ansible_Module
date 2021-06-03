# -*- coding: utf-8
from hw_dme_ansible_core.hostgroup import add
from hw_dme_ansible_core.ansible_base import AnsibleBase
from hw_dme_ansible_core.common import ScriptException
from hw_dme_ansible_core import constants
from ansible.module_utils.basic import AnsibleModule
from hw_dme_ansible_core.ansible_base import ARGUMENT_SPEC_BASE

DOCUMENTATION = r'''
---
module: hostgroup_create
description:
  - Create a host group.
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
  name:
    description:
      - Host group name.
      - Parameter length: 1 to 255.
    type: str
    required: true
  host_ids:
    description:
      - Host ID list.
      - Parameter length: 1 to 64.
    type: str
    required: true
  azs:
    description:
      - AZ ID list.
      - Parameter length: 1 to 64.
    type: str
    required: false
  project_id:
    description:
      - Project ID.
      - Parameter length: 1 to 64.
    type: str
    required: false
  description:
    description:
      - Host group description.
      - Parameter length: 0 to 63.
    type: str
    required: false
'''


def run_module(params, ansible_base, module):
    def create_host_group_request_func(param):
        return ansible_base.post(constants.HOSTGROUP_CREATE_URL, param)

    result = {}

    try:
        result['data'] = add(params, create_host_group_request_func)
        result['msg'] = 'Host group is successfully create.'
    except ScriptException as ex:
        result['msg'] = 'Host group fails to be create. Fault cause: %s.' % ex
        result['failed'] = True
    module.exit_json(**result)


def main():
    argument_spec = dict(
        name=dict(required=True, type='str'),
        host_ids=dict(required=True, type='str'),
        azs=dict(required=False, type='str'),
        project_id=dict(required=False, type='str'),
        description=dict(required=False, type='str')
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
