import os
import vcflat.VcfParse as VP


def get_input():
    nested = {
        "dictA": {"key_1": {"subkey1": "neststuff"}},
        "dictB": {"key_2": "value_2"},
    }
    return nested


def base_tests():
    out = VP.flatten_d(get_input())
    print(out)
    return out


def test_1():
    assert type(base_tests()) is dict


def test_2():
    """ make sure the subdict is no longer nested"""
    assert base_tests()["dictA"] is not dict
