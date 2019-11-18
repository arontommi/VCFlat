import os
import unittest

from pancakevcf.VcfParse import *

class TestVcfParse(unittest.TestCase):

    def setUp(self):
        self.HERE = os.path.dirname(__file__)
        self.VCF_PATH = os.path.join(self.HERE, "test.vcf.gz")
        self.vp = VcfParse(self.VCF_PATH)
        self.df = self.vp.main_parse(input_vcf=self.VCF_PATH)

    def test_flatten(self):
        """
        test if final pandas dataframe is returned and in the correct shape
        """
        self.assertEqual(str(type(self.df)), "<class 'pandas.core.frame.DataFrame'>")
        self.assertEqual(self.df.shape, (115, 1587))

    def test_base(self):
        """
        Test if the first 9 columns are what they are supposed to be
        :return:
        """
        self.assertEqual(self.vp.vcf_header[:9],['#CHROM',
                                            'POS',
                                            'ID',
                                            'REF',
                                            'ALT',
                                            'QUAL',
                                            'FILTER',
                                            'INFO',
                                            'FORMAT'])