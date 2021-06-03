# -*- coding: utf-8
from hw_dme_ansible_core.hostgroup import query
from hw_dme_ansible_core.ansible_base import AnsibleBase
from hw_dme_ansible_core.common import ScriptException
from hw_dme_ansible_core import constants
from ansible.module_utils.basic import AnsibleModule
from hw_dme_ansible_core.ansible_base import ARGUMENT_SPEC_BASE

DOCUMENTATION = r'''
---
module: hostgroup_querys
description:
  - Query host groups in batches.
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
  limit:
    description:
      - Number of records to be displayed on each page.
    type: str
    required: false
  start:
    description:
      - Start position of pagination query.
    type: str
    required: false
  sort_dir:
    description:
      - Sorting order.
      - Value range:
        - asc
        - desc
    type: str
    required: false
  sort_key:
    description:
      - Sorting field.
      - Value range:
        - host_count (number of hosts in a host group)
    type: str
    required: false
  name:
    description:
      - Host group name. Fuzzy match is supported.
      - Parameter length: 1 to 255.
    type: str
    required: false
  project_id:
    description:
      - Project ID.
      - Parameter length: 1 to 64.
    type: str
    required: false
  az_ids:
    description:
      - ID lists of AZs to which the host group belongs.
      - Parameter length: 1 to 64.
    type: str
    required: false
  managed_status:
    description:
      - Takeover status.
      - Value range:
        - UNKNOWN
        - NORMAL
        - TAKE_OVERING
        - TAKE_ERROR
        - TAKE_OVER_ALARM
    type: str
    required: false
'''


def run_module(params, ansible_base, module):
    def host_group_list_request_func(param):
        return ansible_base.post(constants.HOSTGROUP_QUERY_URL, param)

    result = {}

    try:
        result['data'] = query(params, host_group_list_request_func)
        result['msg'] = 'Query host group list successfully.'
    except ScriptException as ex:
        result['msg'] = 'Query host group list failed, Fault cause: %s.' % ex
        result['failed'] = True
    module.exit_json(**result)


def main():
    argument_spec = dict(
        limit=dict(required=False, default='10', type='str'),
        start=dict(required=False, default='0', type='str'),
        sort_dir=dict(required=False, type='str'),
        sort_key=dict(required=False, type='str'),
        name=dict(required=False, type='str'),
        project_id=dict(required=False, type='str'),
        az_ids=dict(required=False, type='str'),
        managed_status=dict(required=False, type='str')
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
