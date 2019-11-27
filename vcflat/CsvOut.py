from vcflat.VcfParse import VcfParse



def generatecsv(input_vcf, outputfile, sample=None,keys=False, fastkeys=True):
    vp = VcfParse(input_vcf)
    if keys:
        vp.write2csv(outputfile, keys,sample)
    if fastkeys:
        print("using the first row to determine column names, "
              "if you are missing something, use fastkeys=FALSE")
        keys = vp.get_header_fast()
        vp.write2csv(outputfile, keys,sample)
    else:
        print("Since no keys were given, all keys need to be determined "
              "and they will all be spit out")
        keys = vp.get_header()
        vp.write2csv(outputfile, keys,sample)



