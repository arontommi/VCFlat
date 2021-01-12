import vcflat.VcfParse as VP
import os

def get_input():
    test_data_dir = os.path.join(os.path.dirname(__file__), '..', 'test_data')
    i = os.path.join(test_data_dir, "test.snpeff.vcf")
    vcffile = VP.VcfParse(i)
    testline = VP.zipformat(VP.nestlists(['','','','','','','','','GT:AD:DP:GQ:PL','0/0:2,0:2:6.01:0,6,6']),
                            header_list=vcffile.vcf_meta.header)
    return vcffile,testline


def base_tests():
    vcffile, testline = get_input()
    return vcffile.split_ref_alt(testline)



def test_1():
    """check if the dict generated has correct nr of elements """
    ref_alt = base_tests()
    assert len(ref_alt) is 10