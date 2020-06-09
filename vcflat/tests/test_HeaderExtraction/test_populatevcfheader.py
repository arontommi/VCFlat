import os
import vcflat.HeaderExtraction as HE

def get_input():
    test_data_dir = os.path.join(os.path.dirname(__file__), '..', 'test_data')
    i = os.path.join(test_data_dir, "test.snpeff.vcf")
    return i


def base_tests():
    header = HE.populatevcfheader(get_input())
    print(header.header)
    return header


def test_1():
    """ checks that output is list """
    assert type(base_tests().header) is list


def test_2():
    """ checks that output not empty """
    assert base_tests().header is not None

def test_3():
    checklist = ['#CHROM', 'POS', 'ID', 'REF', 'ALT', 'QUAL', 'FILTER', 'INFO', 'FORMAT']
    """ checks if correct things are in the header """
    assert all(i in base_tests().header for i in checklist)