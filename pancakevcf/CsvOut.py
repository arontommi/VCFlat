from pancakevcf.VcfParse import VcfParse
from csv import DictWriter
import pandas as pd

def get_header(input_vcf):
    pars = VcfParse(input_vcf).parse(input_vcf)
    keys = set()
    for d in pars:
        keys.update(d.keys())
    return keys


def get_header_fast(input_vcf):
    pars = VcfParse(input_vcf).parse(input_vcf)
    firstrow = next(pars)
    keys = set(firstrow.keys())
    return keys


def write2csv(input_vcf,outputfile, sample,keys):
    pars = VcfParse(input_vcf).parse(input_vcf)

    file = outputfile
    with open(file, 'w') as csvfile:
        writer = DictWriter(csvfile, keys, delimiter='\t', extrasaction='ignore')
        writer.writeheader()
        nr = 0
        for line in pars:
            writer.writerow(line)
            nr += 1
            if nr % 10000 == 0:
                print(f'{nr} processed')
    df = pd.read_csv(outputfile, sep='\t')
    return df

def generatecsv(input_vcf, outputfile, sample=False,keys=False, fastkeys=True):
    if keys:
        df = write2csv(input_vcf,outputfile,sample, keys)
    if fastkeys:
        print("using the first row to determine column names, if you are missing something, use fastkeys=FALSE")
        keys = get_header_fast(input_vcf)
        df = write2csv(input_vcf,outputfile,sample, keys)
    else:
        print("Since no keys were given, all keys need to be determined and they will all be spit out")
        keys = get_header(input_vcf)
        df = write2csv(input_vcf,outputfile,sample, keys)
    return df
