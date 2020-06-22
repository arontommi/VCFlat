import os
import vcflat.HeaderExtraction as HE
from collections import defaultdict


def get_input():
    test_data_dir = os.path.join(os.path.dirname(__file__), '..', 'test_data')
    i = os.path.join(test_data_dir, "test.snpeff.vcf")
    return i


def base_tests():
    metadict = HE.process_meta_dict(get_input())
    return metadict


def test_1():
    """ checks that output is a default dict """
    assert type(base_tests()) is type(defaultdict())


def test_2():
    """ check if the dict is not empty """

    assert base_tests() is not None

def test_3():
    """ check for base things"""
    print(base_tests()['FORMAT'])
    assert len(base_tests()['FORMAT']) is 5
