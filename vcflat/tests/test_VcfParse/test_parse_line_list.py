import vcflat.VcfParse as VP

import os
from cyvcf2 import VCF

def get_input():
    test_data_dir = os.path.join(os.path.dirname(__file__), '..', 'test_data')
    i = os.path.join(test_data_dir, "test-hemi.vcf")
    vcffile = VP.VcfParse(i)
    return vcffile


def base_tests():
    file = get_input()
    vcf_file = VCF('{}'.format(file.input_vcf), strict_gt=True)
    firstline = [i for i in vcf_file][0]
    split_line = [i.strip('\n') for i in str(firstline).split('\t')]
    return file.parse_line_list(split_line)


def test_1():
    assert len(base_tests()) is 37

def test_2():
    test = {'#CHROM', 'POS', 'Transcript', 'CSQ'}
    assert (test.intersection(set((base_tests().keys()))))