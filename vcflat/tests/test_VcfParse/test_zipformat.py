import vcflat.VcfParse as VP
import os


def get_input():
    test_data_dir = os.path.join(os.path.dirname(__file__), "..", "test_data")
    i = os.path.join(test_data_dir, "test.snpeff.vcf")
    testline = VP.nestlists(
        ["", "", "", "", "", "", "", "", "GT:AD:DP:GQ:PL", "0/0:2,0:2:6.01:0,6,6"]
    )
    return i, testline


def base_tests():
    i, testline = get_input()
    vcffile = VP.VcfParse(i)

    return VP.zipformat(testline, header_list=vcffile.vcf_meta.header)


def test_1():
    """check if the dict generated has correct nr of elements """
    assert len(base_tests()[9]) is 5
