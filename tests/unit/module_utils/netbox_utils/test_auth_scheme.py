from __future__ import absolute_import, division, print_function

__metaclass__ = type

import pytest

from ansible_collections.netbox.netbox.plugins.module_utils.netbox_utils import (
    get_auth_scheme,
)


@pytest.mark.parametrize(
    "token, expected",
    [
        ("0123456789abcdef0123456789abcdef01234567", "Token"),
        ("nbt_abc123.0123456789abcdef", "Bearer"),
        ("", "Token"),
        (None, "Token"),
    ],
)
def test_get_auth_scheme(token, expected):
    assert get_auth_scheme(token) == expected
