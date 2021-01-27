import vcflat.VcfParse as VP


def base_tests():
    return VP.nestlists(
        ["", "", "", "", "", "", "", "", "GT:AD:DP:GQ:PL", "0/0:2,0:2:6.01:0,6,6"]
    )


def test_1():
    """check if it is combined """
    assert len(base_tests()[9]) is 2
