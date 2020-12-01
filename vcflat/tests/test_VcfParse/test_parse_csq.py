import vcflat.VcfParse as VP
import os

def get_input():
    testline = ["chr1",
                "30548",
                ".",
                "T",
                "G",
                "50.09",
                ".",
                "CSQ=synonymous_variant|tgC/tgT|C|ENSG00000130164|LDLR|ENST00000558013|2/18|||27/858|protein_coding,synonymous_variant|tgC/tgT|C|ENSG00000130164|LDLR|ENST00000545707|2/16|||27/682|protein_coding,non_coding_transcript_exon_variant&non_coding_transcript_variant|||ENSG00000130164|LDLR|ENST00000557958|2/3||||retained_intron",
                "GT:AD:DP:GQ:PL",
                "./.	./.	./.	./."]

    test_data_dir = os.path.join(os.path.dirname(__file__), '..', 'test_data')
    i = os.path.join(test_data_dir, "test-hemi.vcf")
    return i, testline


def base_tests():
    vcf, testline = get_input()
    vcffile = VP.VcfParse(vcf)
    testline = VP.generate_vaf(
                    VP.split_ref_alt(
                        VP.zipformat(VP.nestlists(testline),header_list=vcffile.vcf_meta.header)))

    testline = VP.splitinfo(testline)
    data = VP.parse_csq(testline, vcffile.csq_labels, 'CSQ')
    return data

def test_1():
    """check if the dict generated has correct nr of elements """
    assert type(base_tests()[0][10]) is dict

def test_2():
    """check if the dict generated has correct nr of elements """
    assert (base_tests()[0][10]) is not None

def test_3():
    """ test to check the multiparsing aspect"""
    pass