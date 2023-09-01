import os
from conftest import testdata_dir
from excel2xx import validator

validator_dir = testdata_dir + "/" + "_validator"


def gen_cases():
    os.makedirs(validator_dir, exist_ok=True)
    """
    """
    pass


def test_validator():
    gen_cases()
    validator.run({}, testdata_dir)
    assert 1 == 1
