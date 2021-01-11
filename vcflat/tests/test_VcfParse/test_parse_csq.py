import vcflat.VcfParse as VP
import os
from cyvcf2 import VCF

from itertools import product, chain

import pytest

def get_input():
    testline = ["chr1",
                "30548",
                ".",
                "T",
                "G",
                "50.09",
                ".",
                "CSQ=synonymous_variant|tgC/tgT|C|ENSG00000130164|LDLR|ENST00000558013|2/18|||27/858|protein_coding,"
                "synonymous_variant|tgC/tgT|C|ENSG00000130164|LDLR|ENST00000545707|2/16|||27/682|protein_coding,"
                "non_coding_transcript_exon_variant&non_coding_transcript_variant|||ENSG00000130164|LDLR"
                "|ENST00000557958|2/3||||retained_intron",
                "GT:AD:DP:GQ:PL",
                "./.	./.	./.	./."]

    test_data_dir = os.path.join(os.path.dirname(__file__), '..', 'test_data')
    i = os.path.join(test_data_dir, "test-hemi.vcf")
    return i, testline


def base_tests(long_anno=None):
    vcf, testline = get_input()
    vcffile = VP.VcfParse(vcf,long_anno=long_anno)
    testline = VP.generate_vaf(
                    VP.split_ref_alt(
                        VP.zipformat(VP.nestlists(testline), header_list=vcffile.vcf_meta.header)))

    testline = VP.splitinfo(testline)
    data = vcffile.parse_csq(testline, vcffile.csq_labels, 'CSQ')
    return data

def test_1():
    """check integrity of output """
    results = base_tests()
    assert type(results) is list
    assert type(results[0]) is dict
    assert len(results) == 3


def test_2():
    """" Checks the validity of the parsing """
    results = base_tests()
    correct = {'Consequence': 'synonymous_variant', 'Codons': 'tgC/tgT', 'Amino_acids': 'C', 'Gene': 'ENSG00000130164',
               'SYMBOL': 'LDLR', 'Feature': 'ENST00000558013', 'EXON': '2/18', 'PolyPhen': '', 'SIFT': '',
               'Protein_position': '27/858', 'BIOTYPE"': 'protein_coding'}
    assert results[0] == correct

def test_3():
    """ Check if to long annotation is removed"""
    results = base_tests(long_anno=1)
    assert results[0]['Consequence'] == "To Long Annotation"


