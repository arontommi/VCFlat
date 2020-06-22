import os
import vcflat.VcfParse as VP

def get_input():
    test_data_dir = os.path.join(os.path.dirname(__file__), '..', 'test_data')
    i = os.path.join(test_data_dir, "test.snpeff.vcf")
    return i

def base_tests():
    i = get_input()
    vcffile = VP.VcfParse(i)
    return vcffile

def test_1():
    """ test if csq flag ist as expected"""
    assert base_tests().csq_flag() is True

