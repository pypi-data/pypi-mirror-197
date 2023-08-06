# -*- coding: utf-8 -*-

"""Test that all modules are importable.
"""

import dknorway
import dknorway.admin
import dknorway.apps
import dknorway.jobs
import dknorway.jobs.monthly
import dknorway.jobs.monthly.posten_postnrimport
import dknorway.models
import dknorway.postnrcache


def test_import_dknorway():
    """Test that all modules are importable.
    """
    
    assert dknorway
    assert dknorway.admin
    assert dknorway.apps
    assert dknorway.jobs
    assert dknorway.jobs.monthly
    assert dknorway.jobs.monthly.posten_postnrimport
    assert dknorway.models
    assert dknorway.postnrcache
