from vcflat.VcfParse import VcfParse

from vcflat.HeaderExtraction import VcfHeader


class OutputHandle:
    def __init__(self, inputfile, outputfile, keys=None, slowkeys=True, sample="Sample", annotation=None,
                 long_anno=None, samples_in_header=None):
        vcffile = VcfParse(inputfile, annotation=annotation, long_anno=long_anno, samples_in_header=samples_in_header)
        if keys:
            keylist = vcffile.sanitize_keys(keys=keys)
        elif slowkeys:
            keylist = vcffile.get_header()
        else:
            keylist = vcffile.get_header_fast()
        if annotation:
            print(f"Extracting {annotation} from info column ")
        if outputfile:
            print(f" Using these keys as column names : {keylist}")
            print(f" Using {sample} for the name column ")
            print(f" saving to {outputfile} as output location")

        vcffile.write2csv(outputfile, keylist, sample)


class OutputPPrint:
    def __init__(self, inputfile):
        VcfHeader(inputfile).pprint_meta()


class OutputPPrintBodyHeader:
    def __init__(self, inputfile):
        VcfHeader(inputfile).pprint_vcf_body_header()
