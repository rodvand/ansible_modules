#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2024, Martin Rødvand (@rodvand)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: netbox_data_source
short_description: Creates or removes Data Sources from NetBox
description:
  - Creates or removes data sources from NetBox
notes:
  - Tags should be defined as a YAML list
  - This should be ran with connection C(local) and hosts C(localhost)
author:
  - Martin Rødvand (@rodvand)
requirements:
  - pynetbox
version_added: "3.20.0"
extends_documentation_fragment:
  - netbox.netbox.common
options:
  data:
    type: dict
    description:
      - Defines the Data Source configuration
    suboptions:
      name:
        description:
          - Name of the Data Source to be created.
        required: true
        type: str    
      type:
        description:
          - Type of the Data Source to be created.
        required: true
        choices:
          - local
          - git
          - amazon-s3
        type: str    
      source_url:
        description:
          - Source URL for the Data Source.
        required: true
        type: str
      enabled:
        description:
          - If the Data Source should be enabled.
        required: false
        type: bool
      description:
        description:
          - Short description for the Data Source.
        required: false
        type: str 
      comments:
        description:
          - Comments for the Data Source. This can be markdown syntax.
        required: false
        type: str
      parameters:
        description:
          - Parameters for the Data Source.
        required: false
        type: dict
      ignore_rules:
        description:
          - Ignore rules for the Data Source.
        required: false
        type: str      
      custom_fields:
        description:
          - must exist in NetBox
        required: false
        type: dict
    required: true
"""

EXAMPLES = r"""
- name: "Test NetBox module"
  connection: local
  hosts: localhost
  gather_facts: false
  tasks:
    - name: Create a local data source within NetBox with only required information
      netbox.netbox.netbox_data_source:        
        data:
          name: Data Source 1
          type: local
          source_url: file:///opt/scripts
        state: present

    - name: Create data source with ignore rules
      netbox.netbox.netbox_data_source:               
        data:
          name: Data Source 1
          type: local
          source_url: file:///opt/scripts
          ignore_rules: "*.txt\n*.dat"
        state: present

    - name: Delete Data Source      
      netbox.netbox.netbox_data_source:               
        data:
          name: Data Source 1
        state: absent

    - name: Create Data Source with parameters
      netbox.netbox.netbox_data_source:                       
        data:
          name: AWS data source          
          type: amazon-s3
          source_url: https://aws-url
          parameters:
            aws_access_key_id: 1234567
            aws_secret_access_key: 89101112
        state: present
"""

RETURN = r"""
data_source:
  description: Serialized object as created or already existent within NetBox
  returned: on creation
  type: dict
msg:
  description: Message indicating failure or info about what has been achieved
  returned: always
  type: str
"""

from ansible_collections.netbox.netbox.plugins.module_utils.netbox_utils import (
    NetboxAnsibleModule,
    NETBOX_ARG_SPEC,
)
from ansible_collections.netbox.netbox.plugins.module_utils.netbox_core import (
    NetboxCoreModule,
    NB_DATASOURCES,
)
from copy import deepcopy


def main():
    """
    Main entry point for module execution
    """
    argument_spec = deepcopy(NETBOX_ARG_SPEC)
    argument_spec.update(
        dict(
            data=dict(
                type="dict",
                required=True,
                options=dict(
                    name=dict(required=True, type="str"),
                    type=dict(
                        required=True, type="str", choices=["local", "git", "amazon-s3"]
                    ),
                    source_url=dict(required=True, type="str"),
                    enabled=dict(required=False, type="bool"),
                    description=dict(required=False, type="str"),
                    comments=dict(required=False, type="str"),
                    parameters=dict(required=False, type="dict"),
                    ignore_rules=dict(required=False, type="str"),
                    custom_fields=dict(required=False, type="dict"),
                ),
            ),
        )
    )

    required_if = [("state", "present", ["name", "type", "source_url"]), ("state", "absent", ["name"])]

    module = NetboxAnsibleModule(
        argument_spec=argument_spec, supports_check_mode=True, required_if=required_if
    )

    netbox_data_source = NetboxCoreModule(module, NB_DATASOURCES)
    netbox_data_source.run()


if __name__ == "__main__":  # pragma: no cover
    main()
