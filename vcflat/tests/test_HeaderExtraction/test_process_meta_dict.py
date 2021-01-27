import os
from collections import defaultdict

from vcflat.HeaderExtraction import VcfHeader


def get_input():
    test_data_dir = os.path.join(os.path.dirname(__file__), "..", "test_data")
    i = os.path.join(test_data_dir, "test.snpeff.vcf")
    vcfh = VcfHeader(i)
    output = vcfh.process_meta_dict()
    return output


def test_1():
    """ checks that output is a default dict """
    assert type(get_input()) is type(defaultdict())


def test_2():
    """ check if the dict is not empty """

    assert get_input() is not None


def test_3():
    """ check for base things"""
    assert len(get_input()["FORMAT"]) is 5
