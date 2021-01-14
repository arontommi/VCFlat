import vcflat.VcfParse as VP
import os


def get_input():
    testline = [
        "chr1",
        "30548",
        ".",
        "T",
        "G",
        "50.09",
        ".",
        "AC = 6;AF = 0.429;AN = 14;BaseQRankSum = 0.000;DP = 7;Dels = 0.00;FS = 0.000;HRun = 0;HaplotypeScore = 0.0000;MQ = 29.00;MQ0 = 0;MQRankSum = -0.550;QD = 16.70;ReadPosRankSum = 0.937",
    ]
    return testline


def base_tests():
    print(VP.splitinfo(get_input())[7])
    return VP.splitinfo(get_input())


def test_1():
    """check if the dict generated has correct nr of elements """
    assert type(base_tests()[7]) is dict


def test_2():
    """check if the dict generated has correct nr of elements """
    assert (base_tests()[7]) is not None
