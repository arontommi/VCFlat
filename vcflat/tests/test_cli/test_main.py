import os


pytest_plugins = ["pytester"]

def get_input():
    test_data_dir = os.path.join(os.path.dirname(__file__), '..', 'test_data')
    input = os.path.join(test_data_dir, "test.snpeff.vcf")

    output = os.path.join(os.path.join(os.path.dirname(__file__), '..', 'test_data'), 'out.csv')
    return input, output

def base_tests():
    input, output = get_input()
    keys = "'CHROM POS'"
    os.system(f' python -m vcflat -i {input} -o {output} --keys {keys}')
    return output

def test_1():
    output = base_tests()
    assert os.path.isfile(output) is True
    os.remove(output)
