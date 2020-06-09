import os
import vcflat.HeaderExtraction as HE


def get_input(file):
    test_data_dir = os.path.join(os.path.dirname(__file__), '..', 'test_data')
    i = os.path.join(test_data_dir, f"{file}")
    return i

def base_test_1():
    i = get_input('test.snpeff.vcf')
    output = HE.get_raw_header(i)
    clean = HE.clean_meta(output)
    dictified = HE.dictify(clean)
    out = HE.custom_dict_chunking(dictified, "FILTER", 1)

    return out

def base_test_2():
    i = get_input('test.snpeff.vcf')
    output = HE.get_raw_header(i)
    clean = HE.clean_meta(output)
    dictified = HE.dictify(clean)
    out = HE.custom_dict_chunking(dictified, "FILTER", 3)
    print(out['FILTER'])
    return out


def test_1():
    """ test if string is split the correct way """
    assert len(base_test_1()['FILTER'][0]) is 2

def test_2():
    """ test if string is split the wrong way  """
    assert len(base_test_2()['FILTER'][0][0]) is not 4