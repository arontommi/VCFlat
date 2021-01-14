import os
from vcflat.HeaderExtraction import get_raw_header, clean_meta


def get_input():
    test_data_dir = os.path.join(os.path.dirname(__file__), "..", "test_data")
    i = os.path.join(test_data_dir, "test.snpeff.vcf")
    return i


def base_tests():
    i = get_input()
    output = get_raw_header(i)
    clean = clean_meta(output)
    return clean


def test_1():
    """ checks that output is list """
    assert type(base_tests()) is list


def test_2():
    """ checks that output is not empty """
    assert len(base_tests()) != 0


def test_3():
    """ checks meta has been cleaned"""
    for i in ["=<", "##"]:
        assert i not in base_tests()
