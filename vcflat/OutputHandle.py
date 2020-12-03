from vcflat.VcfParse import VcfParse


class OutputHandle:
    def __init__(self, inputfile,outputfile, keys=None, slowkeys=True, sample="Sample",annotation=None):
        vcffile = VcfParse(inputfile,annotation=annotation)
        if keys:
            keylist = vcffile.sanitize_keys(keys=keys)
        elif slowkeys:
            keylist = vcffile.get_header()
        else:
            keylist = vcffile.get_header_fast()
        if annotation:
            print(f"Exracting {annotation} from info column ")
        if outputfile:
            print(f" Using these keys as column names : {keylist}")
            print(f" Using {sample} for the name column ")
            print(f" saving to {outputfile} as output location")

        vcffile.write2csv(outputfile, keylist, sample)





