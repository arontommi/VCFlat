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
                "EFF=DOWNSTREAM(MODIFIER||||85|FAM138A|protein_coding|CODING|ENST00000417324|)",
                "GT:AD:DP:GQ:PL",
                "./.	./.	./.	./."]

    test_data_dir = os.path.join(os.path.dirname(__file__), '..', 'test_data')
    i = os.path.join(test_data_dir, "test.snpeff.vcf")
    return i, testline


def base_tests():
    vcf, testline = get_input()
    vcffile = VP.VcfParse(vcf)
    testline = VP.generate_vaf(
                    VP.split_ref_alt(
                        VP.zipformat(
                            VP.nestlists(testline),
                            header_list=vcffile.vcf_meta.header)))

    testline = VP.splitinfo(testline)
    return VP.parse_csq(testline, vcffile.csq_labels, 'EFF')


def test_1():
    """check if the dict generated has correct nr of elements """
    assert type(base_tests()[10]) is dict

def test_2():
    """check if the dict generated has correct nr of elements """
    assert (base_tests()[10]) is not None