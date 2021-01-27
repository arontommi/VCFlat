import os
import pytest
import sys


def get_input():
    test_data_dir = os.path.join(os.path.dirname(__file__), "..", "test_data")
    input = os.path.join(test_data_dir, "test.snpeff.vcf")

    output = os.path.join(
        os.path.join(os.path.dirname(__file__), "..", "test_data"), "out.csv"
    )
    return input, output


def test_1(capsys):
    "Simple 'does this file create the file at correct place'"
    input, output = get_input()
    keys = "'#CHROM POS'"
    os.system(f" python3 -m vcflat -i {input} --keys {keys}")
    captured = capsys.readouterr()
    assert captured.out is not None
