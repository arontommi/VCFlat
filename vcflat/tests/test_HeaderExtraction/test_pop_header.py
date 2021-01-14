import os
from vcflat.HeaderExtraction import get_raw_header, extract_header, pop_header


def get_input():
    test_data_dir = os.path.join(os.path.dirname(__file__), "..", "test_data")
    i = os.path.join(test_data_dir, "test.snpeff.vcf")
    return i


def get_no_chrom():
    i = get_input()
    output = get_raw_header(i)
    output_no_chrom = pop_header(output)
    return output_no_chrom


def test_1():
    """ checks that output is list """
    assert type(get_no_chrom()) is list


def test_2():
    """ checks that output is not empty """
    assert len(get_no_chrom()) != 0


def test_3():
    """ checks that the header has been poped """
    header = extract_header(get_input())
    assert header not in get_no_chrom()
