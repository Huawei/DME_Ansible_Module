# -*- coding: utf-8
from hw_dme_ansible_core.volume import query
from hw_dme_ansible_core.ansible_base import AnsibleBase
from hw_dme_ansible_core.common import ScriptException
from hw_dme_ansible_core import constants
from ansible.module_utils.basic import AnsibleModule
from hw_dme_ansible_core.ansible_base import ARGUMENT_SPEC_BASE

DOCUMENTATION = r'''
---
module: lun_query
description:
  - Query LUNs in batches.
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
  offset:
    description:
      - Start position of pagination query.
    type: str
    required: false
  sort_dir:
    description:
      - Sorting order
      - Value range:
        - asc
        - desc
    type: str
    required: false
  sort_key:
    description:
      - Sorting field
      - Value range:
        - capacity
    type: str
    required: false
  name:
    description:
      - LUN name. Fuzzy query is supported.
      - Parameter length: 1 to 255.
    type: str
    required: false
  status:
    description:
      - LUN status.
      - Value range:
        - creating
        - normal
        - mapping
        - unmapping
        - deleting
        - error
        - expanding
    type: str
    required: false
  service_level_id:
    description:
      - Service level ID.
      - Parameter length: 1 to 64.
    type: str
    required: false
  volume_wwn:
    description:
      - LUN WWN.
      - Parameter length of each WWN: 1 to 64.
    type: str
    required: false
  storage_id:
    description:
      - Storage device ID.
      - Parameter length: 1 to 64.
    type: str
    required: false
  pool_raw_id:
    description:
      - ID of a storage pool on the storage device.
      - Parameter length: 1 to 64.
    type: str
    required: false
  host_id:
    description:
      - Host ID.
      - Parameter length: 1 to 64.
    type: str
    required: false
  hostgroup_id:
    description:
      - Host group ID.
      - Parameter length: 1 to 64.
    type: str
    required: false
  unmapped_host_id:
    description:
      - IDs of hosts without mapped LUNs.
      - Parameter length: 1 to 64.
    type: str
    required: false
  unmapped_hostgroup_id:
    description:
      - IDs of host groups without mapped LUNs.
      - Parameter length: 1 to 64.
    type: str
    required: false
  project_id:
    description:
      - Project ID.
      - Parameter length: 1 to 64.
    type: str
    required: false
  allocate_type:
    description:
      - Allocation type.
      - Value range:
        - thin
        - thick
    type: str
    required: false
  attached:
    description:
      - Mapping status.
      - Value range:
        - service (querying LUNs provisioned as services)
        - non-service (querying LUNs provisioned as non-services)
        - all (querying all LUNs)
    type: str
    required: false
  query_mode:
    description:
      - LUN provisioning mode
    type: str
    required: false
  protected:
    description:
      - Protection status of the LUN.
    type: str
    required: false
  pg_id:
    description:
      - Protection group ID.
      - Parameter length: 1 to 64.
    type: str
    required: false
'''


def run_module(params, ansible_base, module):
    def query_luns_request_func(param):
        return ansible_base.get(constants.LUN_QUERY_URL, param)

    result = {}

    try:
        result['data'] = query(params, query_luns_request_func)
        result['msg'] = 'Query LUNs successfully.'
    except ScriptException as ex:
        result['msg'] = 'Query LUNs failed, Fault cause: %s.' % ex
        result['failed'] = True
    module.exit_json(**result)


def main():
    argument_spec = dict(
        limit=dict(required=False, default='10', type='str'),
        offset=dict(required=False, default='0', type='str'),
        sort_dir=dict(required=False, type='str'),
        sort_key=dict(required=False, type='str'),
        name=dict(required=False, type='str'),
        status=dict(required=False, type='str'),
        service_level_id=dict(required=False, type='str'),
        volume_wwn=dict(required=False, type='str'),
        storage_id=dict(required=False, type='str'),
        pool_raw_id=dict(required=False, type='str'),
        host_id=dict(required=False, type='str'),
        hostgroup_id=dict(required=False, type='str'),
        unmapped_host_id=dict(required=False, type='str'),
        unmapped_hostgroup_id=dict(required=False, type='str'),
        project_id=dict(required=False, type='str'),
        allocate_type=dict(required=False, type='str'),
        attached=dict(required=False, type='str'),
        query_mode=dict(required=False, type='str'),
        protected=dict(required=False, type='str'),
        pg_id=dict(required=False, type='str')
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
