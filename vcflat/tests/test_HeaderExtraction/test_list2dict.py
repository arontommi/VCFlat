from vcflat import HeaderExtraction as HE


def get_input():
    basedict = {"testfield": [["test=split"]]}
    return basedict


def base_test1():
    input = get_input()
    output = HE.list2dict(input, "testfield")
    return output


def test_1():
    assert type(base_test1()) is type(dict())
