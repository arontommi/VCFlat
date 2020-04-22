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
    validated = HE.validate_meta(dictified)
    return validated

def base_test_2():
    i = get_input('invalid.vcf')
    output = HE.get_raw_header(i)
    clean = HE.clean_meta(output)
    dictified = HE.dictify(clean)
    validated = HE.validate_meta(dictified)
    return validated

def test_1():
    """ validate that true is returned on a valid vcf """
    assert base_test_1() is True

def test_2():
    """ validate that false is returned on a invalid vcf """
    assert base_test_2() is False




