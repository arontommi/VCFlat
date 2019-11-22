import os
import unittest

from pancakevcf.VcfParse import *

class TestVcfParse(unittest.TestCase):

    def setUp(self):
        self.HERE = os.path.dirname(__file__)
        self.VCF_PATH = os.path.join(self.HERE, "test.vcf.gz")
        self.vp_1 = VcfParse(self.VCF_PATH)
        self.VCF_PATH = os.path.join(self.HERE, "issue_44.vcf")
        self.vp_2 = VcfParse(self.VCF_PATH)


    def test_flatten(self):
        """
        test if final pandas dataframe is returned and in the correct shape
        """
        self.assertEqual(str(type(self.vp_1.df)), "<class 'pandas.core.frame.DataFrame'>")
        self.assertEqual(self.vp_1.df.shape, (115, 1966))

    def test_base(self):
        """
        Test if the first 9 columns are what they are supposed to be
        :return:
        """
        self.assertEqual(self.vp_1.vcf_meta.header[:8],['#CHROM',
                                            'POS',
                                            'ID',
                                            'REF',
                                            'ALT',
                                            'QUAL',
                                            'FILTER',
                                            'INFO'])

