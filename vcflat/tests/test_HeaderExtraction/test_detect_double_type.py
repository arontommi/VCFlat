import os
import vcflat.HeaderExtraction as HE

def get_input():
    test_data_dir = os.path.join(os.path.dirname(__file__), '..', 'test_data')
    i = os.path.join(test_data_dir, "test.snpeff.vcf")
    return i


def base_tests():
    dict_with_double_type_specified = HE.detect_double_type(get_input())
    return dict_with_double_type_specified

def test_1():
    dtd =base_tests()
    assert dtd['FORMAT']['AD']['double_type'] == 'REF_ALT'
