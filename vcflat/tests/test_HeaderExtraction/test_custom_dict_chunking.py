import os

from vcflat.HeaderExtraction import VcfHeader, dictify, clean_meta, custom_dict_chunking

# TODO add more tests that make more sense


def get_input():
    test_data_dir = os.path.join(os.path.dirname(__file__), "..", "test_data")
    i = os.path.join(test_data_dir, "test.snpeff.vcf")
    return i


def base_test(nr):
    vch = VcfHeader(get_input())
    output = vch.get_raw_header()
    clean = clean_meta(output)
    dictified = dictify(clean)
    out = custom_dict_chunking(dictified, "FILTER", nr)
    return out


def test_1():
    """ test if string is split the correct way """
    assert len(base_test(1)["FILTER"][0]) is 2


def test_2():
    """ test if string is split the wrong way  """
    assert len(base_test(3)["FILTER"][0][0]) is not 4
