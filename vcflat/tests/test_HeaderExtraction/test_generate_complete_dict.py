import os
import vcflat.HeaderExtraction as HE
from collections import defaultdict

def get_input():
    test_data_dir = os.path.join(os.path.dirname(__file__), '..', 'test_data')
    i = os.path.join(test_data_dir, "test.snpeff.vcf")
    raw_header = HE.get_raw_header(i)
    raw_header_popped = HE.pop_header(raw_header)
    cleaned_meta = HE.clean_meta(raw_header_popped)
    base_dict = HE.dictify(cleaned_meta)
    return base_dict


def base_tests():
    base_dict = get_input()
    dict = HE.generate_complete_dict(base_dict, "INFO", 3)
    return dict


def test_1():
    """ checks that output is list """
    assert type(base_tests()) is type(defaultdict())

def test_2():
    """ checks that output is list """
    assert type(base_tests()['INFO']) is not None

def test_3():
    """ checks that output is list """
    assert len(base_tests()['INFO']['AC']) is 3