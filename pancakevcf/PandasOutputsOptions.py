#TODO store what pandas columns to return

class BareProfile:
    """
    only the most simple view of the pandas df
    """
    columns = ['#CHROM','POS','REF','ALT','FILTER']

class SimpleProfile:
    """
    Simple view with gene name, if it is exonic and if it is bad.
    """
    columns = BareProfile.columns + ['SYMBOL',
                                     'Gene',
                                     'IMPACT',
                                     'Consequence',
                                     'Existing_variation']

class SampleSpecificColumns:
    """
    Extract columns of that are specific to each sample from df
    """
    def __init__(self, vcfparse):
        self.df = vcfparse.df
        self.sample_header = vcfparse.sample_header
        if vcfparse.csq:
            self.columns = SimpleProfile.columns + self.get_sample_specific_cols()
        else:
            self.columns = BareProfile.columns + self.get_sample_specific_cols()

    def get_sample_specific_cols(self):
        sample_specific_cols = []
        for i in self.sample_header:
            for ii in list(self.df.columns.values):
                if ii.startswith(i):
                    sample_specific_cols.append(ii)
        return sample_specific_cols











