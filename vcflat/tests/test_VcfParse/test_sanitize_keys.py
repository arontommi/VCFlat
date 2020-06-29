import vcflat.VcfParse as VP
import os


def get_input():
    test_data_dir = os.path.join(os.path.dirname(__file__), '..', 'test_data')
    i = os.path.join(test_data_dir, "test.snpeff.vcf")
    vcffile = VP.VcfParse(i)
    return vcffile

def test_1():
    """ Check i the keys are found in the header of the vcf and reported correcly back"""
    vcffile = get_input()
    keys = '#CHROM POS'
    sanitized_keys = vcffile.sanitize_keys(keys)
    assert sanitized_keys == ["#CHROM",'POS']

def test_2():
    """ return None since the key is not in the vcf file"""
    vcffile = get_input()
    keys = '#CHROM POS Wrong_key'
    sanitized_keys = vcffile.sanitize_keys(keys)
    assert sanitized_keys is None