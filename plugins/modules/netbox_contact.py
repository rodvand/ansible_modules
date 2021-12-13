#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2021, Martin Rødvand (@rodvand)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: netbox_contact
short_description: Creates or removes contacts from NetBox
description:
  - Creates or removes contacts from NetBox
notes:
  - Tags should be defined as a YAML list
  - This should be ran with connection C(local) and hosts C(localhost)
author:
  - Martin Rødvand (@rodvand)
requirements:
  - pynetbox
version_added: "3.5.0"
extends_documentation_fragment:
  - netbox.netbox.common
options:
  data:
    type: dict
    description:
      - Defines the contact configuration
    suboptions:
      name:
        description:
          - Name of the contact to be created
        required: true
        type: str
      title:
        description:
          - The title of the contact
        required: false
        type: str
      phone:
        description:
          - The phone number of the contact
        required: false
        type: str
      email:
        description:
          - The email of the contact
        required: false
        type: str
      address:
        description:
          - The address of the contact
        required: false
        type: str
      comments:
        description:
          - Comments on the contact
        required: false
        type: str
      contact_group:
        description:
          - Group assignment for the contact
        required: false
        type: raw
      tags:
        description:
          - Any tags that the contact may need to be associated with
        required: false
        type: list
        elements: raw
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
  gather_facts: False
  tasks:
    - name: Create contact within NetBox with only required information
      netbox_contact:
        netbox_url: http://netbox.local
        netbox_token: thisIsMyToken
        data:
          name: Contact One
        state: present

    - name: Delete contact within netbox
      netbox_tenant:
        netbox_url: http://netbox.local
        netbox_token: thisIsMyToken
        data:
          name: Contact One
        state: absent

    - name: Create tenant with all parameters
      netbox_tenant:
        netbox_url: http://netbox.local
        netbox_token: thisIsMyToken
        data:
          name: Tenant ABC
          tenant_group: Very Special Tenants
          description: ABC Incorporated
          comments: '### This tenant is super cool'
          slug: tenant_abc
          tags:
            - tagA
            - tagB
            - tagC
        state: present
"""

RETURN = r"""
contact:
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
from ansible_collections.netbox.netbox.plugins.module_utils.netbox_tenancy import (
    NetboxTenancyModule,
    NB_CONTACTS,
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
                    title=dict(required=False, type="str"),
                    phone=dict(required=False, type="str"),
                    email=dict(required=False, type="str"),
                    address=dict(required=False, type="str"),
                    comments=dict(required=False, type="str"),
                    contact_group=dict(required=False, type="raw"),
                    tags=dict(required=False, type="list", elements="raw"),
                    custom_fields=dict(required=False, type="dict"),
                ),
            ),
        )
    )

    required_if = [("state", "present", ["name"]), ("state", "absent", ["name"])]

    module = NetboxAnsibleModule(
        argument_spec=argument_spec, supports_check_mode=True, required_if=required_if
    )

    netbox_tenant = NetboxTenancyModule(module, NB_CONTACTS)
    netbox_tenant.run()


if __name__ == "__main__":  # pragma: no cover
    main()
