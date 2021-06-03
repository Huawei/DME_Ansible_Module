# -*- coding: utf-8
from hw_dme_ansible_core.host import query
from hw_dme_ansible_core.ansible_base import AnsibleBase
from hw_dme_ansible_core.common import ScriptException
from hw_dme_ansible_core import constants
from ansible.module_utils.basic import AnsibleModule
from hw_dme_ansible_core.ansible_base import ARGUMENT_SPEC_BASE

DOCUMENTATION = r'''
---
module: host_querys
description:
  - Query hosts in batches.
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
      - Number of records to be displayed on each.
    type: str
    required: false
  start:
    description:
      - Start position of pagination query.
    type: str
    required: false
  name:
    description:
      - Host name. Fuzzy match is supported.
      - Parameter length: 1 to 255.
    type: str
    required: false
  sort_key:
    description:
      - Sorting field.
      - Value range:
        - initiator_count (number of initiators)
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
  host_group_name:
    description:
      - Host group name. Fuzzy match is supported.
      - Parameter length: 1 to 255.
    type: str
    required: false
  ip:
    description:
      - Host IP address.
      - Parameter length: 1 to 255.
    type: str
    required: false
  display_status:
    description:
      - Displayed status.
      - Value range:
        - OFFLINE (disconnected)
        - NOT_RESPONDING (no heartbeat responses from the ESXi host)
        - GRAY (unknown ESXi host)
        - NORMAL (normal ESXi host or connected non-ESXi host)
        - RED (abnormal ESXi host)
        - YELLOW (possible abnormal ESXi host)
        - REBOOTING (FusionSphere host being rebooted)
        - INITIAL (FusionSphere host being initialized)
        - BOOTING (FusionSphere host being booted)
        - SHUTDOWNING (FusionSphere host being powered off)
    type: str
    required: false
  managed_status:
    description:
      - Takeover status of the host.
      - Value range:
        - UNKNOWN (reserved)
        - NORMAL (successful)
        - TAKE_OVERING (taking over)
        - TAKE_ERROR (error)
        - TAKE_OVER_ALARM (alarm)
    type: str
    required: false
  os_type:
    description:
      - Host OS type.
      - Value range:
        - UNKNOWN
        - LINUX
        - WINDOWS
        - SUSE
        - EULER
        - REDHAT
        - CENTOS
        - WINDOWSSERVER2012
        - SOLARIS
        - HPUX
        - AIX
        - XENSERVER
        - MACOS
        - VMWAREESX
        - ORACLE
        - OPENVMS
        - ORACLE_VM_SERVER_FOR_X86
        - ORACLE_VM_SERVER_FOR_SPARC
    type: str
    required: false
  access_mode:
    description:
      - Host addition mode.
      - Value range:
        - ACCOUNT
        - NONE
        - VCENTER
        - FUSIONSPHERE
    type: str
    required: false
  az_ids:
    description:
      - ID list of AZs to which the host belong.
      - Parameter length: 1 to 64.
      - Constraint: A maximum of 40IDs are supported.
    type: str
    required: false
  project_id:
    description:
      - Project ID.
      - Parameter length: 1 to 64.
    type: str
    required: false
'''


def run_module(params, ansible_base, module):
    def host_list_request_func(param):
        return ansible_base.post(constants.HOST_QUERY_URL, param)

    result = {}
    try:
        result['data'] = query(params, host_list_request_func)
        result['msg'] = 'Query hosts list successfully.'
    except ScriptException as ex:
        result['msg'] = 'Query hosts list failed, Fault cause: %s.' % ex
        result['failed'] = True
    module.exit_json(**result)


def main():
    argument_spec = dict(
        limit=dict(required=False, type='str', default='10'),
        start=dict(required=False, type='str', default='0'),
        name=dict(required=False, type='str'),
        sort_key=dict(required=False, type='str'),
        sort_dir=dict(required=False, type='str'),
        host_group_name=dict(required=False, type='str'),
        ip=dict(required=False, type='str'),
        display_status=dict(required=False, type='str'),
        managed_status=dict(required=False, type='str'),
        os_type=dict(required=False, type='str'),
        access_mode=dict(required=False, type='str'),
        az_ids=dict(required=False, type='str'),
        project_id=dict(required=False, type='str'),
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
