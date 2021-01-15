import os
from vcflat.HeaderExtraction import VcfHeader


def get_input():
    test_data_dir = os.path.join(os.path.dirname(__file__), "..", "test_data")
    i = os.path.join(test_data_dir, "test.snpeff.vcf")
    vcfh = VcfHeader(i)
    output = vcfh.get_raw_header()
    return output


def test_1():
    """ checks that output is list """
    assert type(get_input()) is list


def test_2():
    """ checks that output is not empty """
    assert len(get_input()) != 0
