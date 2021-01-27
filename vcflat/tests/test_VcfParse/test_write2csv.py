import vcflat.VcfParse as VP
import os


def get_input():
    test_data_dir = os.path.join(os.path.dirname(__file__), "..", "test_data")
    i = os.path.join(test_data_dir, "test.snpeff.vcf")
    vcffile = VP.VcfParse(i)
    out = os.path.join(
        os.path.join(os.path.dirname(__file__), "..", "test_data"), "out.csv"
    )
    return vcffile, out


def base_tests():
    file, out = get_input()
    keys = ["#CHROM", "POS"]

    file.write2csv(out, keys)
    return out


def test_1():
    out = base_tests()
    assert os.path.isfile(out) is True
    os.remove(out)


def test_2():
    out = base_tests()
    base_tests()
    assert os.path.getsize(out) == 672
    os.remove(out)
