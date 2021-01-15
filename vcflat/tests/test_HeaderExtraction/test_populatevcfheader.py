
import os

from vcflat.HeaderExtraction import VcfHeader

def get_input(samples_in_header=None):
    test_data_dir = os.path.join(os.path.dirname(__file__), "..", "test_data")
    i = os.path.join(test_data_dir, "test.snpeff.vcf")
    vcfh = VcfHeader(i, samples_in_header=samples_in_header)

    return vcfh

def test_1():
    """ checks that output is list """
    assert type(get_input().header) is list


def test_2():
    """ checks that output not empty """
    assert get_input().header is not None


def test_3():
    checklist = [
        "#CHROM",
        "POS",
        "ID",
        "REF",
        "ALT",
        "QUAL",
        "FILTER",
        "INFO",
        "FORMAT",
    ]
    """ checks if correct things are in the header """
    assert all(i in get_input().header for i in checklist)


def test_4():
    checklist = [
        "#CHROM",
        "POS",
        "ID",
        "REF",
        "ALT",
        "QUAL",
        "FILTER",
        "INFO",
        "FORMAT",
        "1",
        "2",
        "3",
        "4",
    ]
    assert all(i in get_input(samples_in_header="1 2 3 4").header for i in checklist)
