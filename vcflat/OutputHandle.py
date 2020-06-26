from vcflat.VcfParse import VcfParse


class OutputHandle:
    def __init__(self, inputfile,outputfile, keys=None, slowkeys=True, sample="Sample"):
        vcffile = VcfParse(inputfile)
        if keys:
            keylist = keys.split()
        elif slowkeys:
            keylist = vcffile.get_header()
        else:
            keylist = vcffile.get_header_fast()
        if outputfile:
            print(f" Using these keys as column names : {keylist}")
            print(f" Using {sample} for the name column ")
            print(f" saving to {outputfile} as output location")

        vcffile.write2csv(outputfile, keylist, sample)





