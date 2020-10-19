# -*- coding: utf-8 -*-
import pytest

from validators import *


@pytest.mark.parametrize('value', [
    'GB82WEST12345698765432',
    'NO9386011117947'
])
def test_returns_true_on_valid_iban(value):
    assert iban(value)


@pytest.mark.parametrize('value', [
    'GB81WEST12345698765432',
    'NO9186011117947'
])
def test_returns_failed_validation_on_invalid_iban(value):
    result = iban(value)
    assert isinstance(result, ValidationFailure)
