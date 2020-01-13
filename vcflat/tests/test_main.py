import os
import unittest
import pandas as pd

from vcflat.CsvOut import generatecsv

class TestVcfParse(unittest.TestCase):
    #TODO fix test, make more tests and each test simpler
    def setUp(self):
        self.HERE = os.path.dirname(__file__)
        self.VCF_PATH = os.path.join(self.HERE, "test.vcf.gz")
        self.output = os.path.join(self.HERE, "test.csv")
        generatecsv(self.VCF_PATH,outputfile=self.output, fastkeys=False)
        self.vp_1 = pd.read_table(self.output)
        print(self.vp_1.shape)
        self.VCF_PATH = os.path.join(self.HERE, "issue_44.vcf")
        self.output = os.path.join(self.HERE, "issue_44.csv")
        generatecsv(self.VCF_PATH, outputfile=self.output, fastkeys=False)
        self.vp_2 = pd.read_table(self.output)


    def test_flatten(self):
        """
        test if final pandas dataframe is returned and in the correct shape
        """
        self.assertEqual(str(type(self.vp_1)), "<class 'pandas.core.frame.DataFrame'>")
        self.assertEqual(self.vp_1.shape, (115, 2155))


