
import os
from vcflat.HeaderExtraction import VcfHeader


def get_input():
    test_data_dir = os.path.join(os.path.dirname(__file__), "..", "test_data")
    i = os.path.join(test_data_dir, "test.snpeff.vcf")
    vcfh = VcfHeader(i)
    return vcfh




def test_1():
    dtd = get_input()
    assert dtd.meta_dict["FORMAT"]["AD"]["double_type"] == "REF_ALT"
