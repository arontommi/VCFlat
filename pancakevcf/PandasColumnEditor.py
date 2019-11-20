# TODO create nice new columns with functions from here.
import pandas as pd

class Arithmetic:

    def ad2vaf(self, df):
        """
        search for Allele Depth for ref and rel in the df and create a variant allele frequency tab
        :param vcfparse:

        """
        for i in list(df.columns.values):
            if i.endswith("_AD_REF"):
                sname = i.strip("_AD_REF")
                alt = sname + "_AD_ALT"
                sname_dp = sname + '_DP'
                sname_vaf = sname + '_VAF'
                df[alt] = pd.to_numeric(df[alt])
                df[sname_dp] = pd.to_numeric(df[sname_dp])
                df[sname_vaf] = (df[alt] / df[sname_dp] *100).round(2)
        return df