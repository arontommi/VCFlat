import os
from vcflat.HeaderExtraction import VcfHeader, dictify, clean_meta
from collections import defaultdict


def get_input():
    test_data_dir = os.path.join(os.path.dirname(__file__), "..", "test_data")
    i = os.path.join(test_data_dir, "test.snpeff.vcf")
    return i


def base_tests():
    vch = VcfHeader(get_input())
    output = vch.get_raw_header()
    clean = clean_meta(output)
    dictified = dictify(clean)
    return dictified


def test_1():
    """ checks that output is dict """
    assert type(base_tests()) is type(defaultdict())


def test_2():
    """ checks that output is not empty """
    assert len(base_tests()) != 0
