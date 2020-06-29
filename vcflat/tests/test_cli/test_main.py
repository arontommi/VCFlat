import os, csv


pytest_plugins = ["pytester"]

def get_input():
    test_data_dir = os.path.join(os.path.dirname(__file__), '..', 'test_data')
    input = os.path.join(test_data_dir, "test.snpeff.vcf")

    output = os.path.join(os.path.join(os.path.dirname(__file__), '..', 'test_data'), 'out.csv')
    return input, output

def test_1():
    "Simple 'does this file create the file at correct place'"
    input, output = get_input()
    keys = "'#CHROM POS'"
    os.system(f' python3 -m vcflat -i {input} -o {output} --keys {keys}')
    assert os.path.isfile(output) is True
    os.remove(output)

def test_2():
    exit_status_help = os.system('python -m vcflat --help')
    exit_status_h = os.system('python -m vcflat -h')
    assert exit_status_help == 0
    assert exit_status_h == 0

def test_3():
    """ Test key if correct keys are in the csv returned"""
    input, output = get_input()
    keys = "'#CHROM POS'"
    os.system(f' python -m vcflat -i {input} -o {output} --keys {keys}')

    with open(output, 'r') as f:
        reader = csv.DictReader(f)
        assert keys[1:-1].split() == reader.fieldnames[0].split('\t')
    os.remove(output)

def test_4():
    """ Test key if correct keys are in the csv returned"""
    input, output = get_input()
    with open(os.path.join(os.path.dirname(__file__), '..', 'test_data','main_test4_keys.txt')) as f:
        returnkeys = f.read().splitlines()
    os.system(f' python -m vcflat -i {input} -o {output}')

    with open(output, 'r') as f:
        reader = csv.DictReader(f)
        assert set(returnkeys).issubset(set((reader.fieldnames[0].split('\t'))))
    os.remove(output)
