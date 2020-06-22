import vcflat.VcfParse as VP
import os


def get_input():
    test_data_dir = os.path.join(os.path.dirname(__file__), '..', 'test_data')
    i = os.path.join(test_data_dir, "test.snpeff.vcf")
    vcffile = VP.VcfParse(i)
    return vcffile


def base_tests():
    file = get_input()
    first_line = next(file.parse())

    return first_line


def test_1():
    assert type(base_tests()) is dict

def test_2():
    test = {'1094PC0005_GT', '1094PC0005_AD', '1094PC0005_DP', '1094PC0005_GQ'}
    assert (test.intersection(set((base_tests().keys()))))