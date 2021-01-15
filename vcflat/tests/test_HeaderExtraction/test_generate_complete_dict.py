
import os
from vcflat.HeaderExtraction import VcfHeader, generate_complete_dict
from collections import defaultdict


def get_input():
    test_data_dir = os.path.join(os.path.dirname(__file__), "..", "test_data")
    i = os.path.join(test_data_dir, "test.snpeff.vcf")
    vcfh = VcfHeader(i)
    return vcfh


def test_1():
    """ checks that output is list """
    assert type(get_input().meta_dict['INFO']) is dict


def test_2():
    """ checks that output is list """
    assert type(get_input().meta_dict['INFO']) is not None


def test_3():
    """ checks that output is list """
    assert len(get_input().meta_dict['INFO']["AC"]["data"]) is 3
