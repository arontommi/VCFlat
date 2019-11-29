from vcflat.VcfParse import VcfParse
import csv



def generatecsv(input_vcf, outputfile,samplefield=None, sample=None,keys=False, fastkeys=True):
    vp = VcfParse(input_vcf,samplefield)
    if isinstance(keys, str):
        keys = keys.split()
        print( f'using these keys :{keys}')
        vp.write2csv(outputfile, keys, sample)
    elif fastkeys:
        print("using the first row to determine column names, "
              "if you are missing something, use fastkeys=FALSE")
        keys = vp.get_header_fast()

        print(f'using these keys :{keys}')
        vp.write2csv(outputfile, keys,sample)
    else:
        print("Since no keys were given, all keys need to be determined "
              "and they will all be spit out")
        keys = vp.get_header()
        print(f'using these keys :{keys}')
        vp.write2csv(outputfile, keys,sample)



