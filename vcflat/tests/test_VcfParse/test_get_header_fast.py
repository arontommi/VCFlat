import vcflat.VcfParse as VP
import os


def get_input():
    test_data_dir = os.path.join(os.path.dirname(__file__), "..", "test_data")
    i = os.path.join(test_data_dir, "test-hemi.vcf")
    vcffile = VP.VcfParse(i)
    return vcffile


def base_tests():
    file = get_input()
    header = file.get_header_fast()
    print(len(header))
    return header


def test_1():
    assert type(base_tests()) is set


def test_2():
    assert len(base_tests()) == 282
