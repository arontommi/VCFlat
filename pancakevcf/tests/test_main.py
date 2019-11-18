import os
import unittest

from pancakevcf.VcfParse import *

class TestVcfParse(unittest.TestCase):

    def test_flatten(self):
        """
        test if final pandas dataframe is returned and in the correct shape
        """
        HERE = os.path.dirname(__file__)
        VCF_PATH = os.path.join(HERE, "test.vcf.gz")
        vp = VcfParse(VCF_PATH)
        df = vp.main_parse(input_vcf=VCF_PATH)
        self.assertEqual(str(type(df)), "<class 'pandas.core.frame.DataFrame'>")
        self.assertEqual(df.shape, (115, 1587))
