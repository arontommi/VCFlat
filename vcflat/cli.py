import click

import vcflat.VcfParse as VP

@click.command()
@click.option(
    '--inputfile', '-i',
    help=' VCF file ',
)
@click.option(
    '--outputfile', '-o',
    help=' Name of the output file',
)
@click.option(
    '--sample', '-s',
    help='I you want to rename the samples to something smart',
)
@click.option(
    "--samplefield",
    help='gives the samplefields common names'
)
@click.option(
    '--keys',
    help='keys for columns, select columns to extract and use in the output file'
)
@click.option(
    '--slowkeys',
    help='if you just want to use all keys found in the vcf, else it uses only the ones in the first variant',
    is_flag=True,
    flag_value=True
)
def vcflat(inputfile, outputfile,samplefield=None, sample=None,keys=False, slowkeys=True):

    if not inputfile:
        print("""
            Hey you need to make sure to have an inputfile! please use vcflat --help 
            to get more information
            """
              )
        exit()
    vp = VP.VcfParse(inputfile)
    if isinstance(keys, str):
        keys = keys.split()
        print( f'using these keys :{keys}')
    elif slowkeys:
        print("Since no keys were given, all keys need to be determined "
              "and they will all be spit out")
        keys = vp.get_header()
        print(f'using these keys :{keys}')
    else:
        print("using the first row to determine column names, "
              "if you are missing something, use slowkeys=True")
        keys = vp.get_header_fast()

        print(f'using these keys :{keys}')
    vp.write2csv(outputfile, keys, sample)


if __name__ == '__main__':
    vcflat()