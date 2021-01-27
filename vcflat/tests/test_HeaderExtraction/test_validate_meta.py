import os
from vcflat.HeaderExtraction import VcfHeader, clean_meta, dictify, validate_meta


def get_input(file):
    test_data_dir = os.path.join(os.path.dirname(__file__), "..", "test_data")
    i = os.path.join(test_data_dir, f"{file}")
    vch = VcfHeader(i)
    validated = validate_meta(dictify(clean_meta(vch.get_raw_header())))
    return validated


def test_1():
    """ validate that true is returned on a valid vcf """
    assert all(get_input("test.snpeff.vcf")) is True
