#TODO store what pandas columns to return
from pancakevcf.HeaderExtraction import HeaderExtract


class BaseProfile:
    """
    only the most simple view of the pandas df
    """
    base_columns = ['#CHROM','POS','REF','ALT']
