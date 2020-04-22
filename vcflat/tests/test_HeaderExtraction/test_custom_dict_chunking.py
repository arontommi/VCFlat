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
    out = HE.custom_dict_chunking(dictified, "FORMAT", 3)
    print(out['FORMAT'])
    return out


def test_1():
    """ mak """
    assert len(base_test_1()['FILTER'][0]) is 2

def test_2():
    """ mak """
    assert len(base_test_2()['FORMAT'][0][0]) is 4
