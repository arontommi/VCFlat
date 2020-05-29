from vcflat.VcfParse import VcfParse

import click

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
    """
    Core function about handling input files

    :param inputfile: Any kind of VCF file
    :param outputfile: name of the output file
    :param samplefield: fields after the "INFO" samples
    :param sample: Sample is the name of the specimen so that you can combine multiple vcfs into one csv
    :param keys: what keys to select from the vcf file
    :param slowkeys: if you just want to use all keys from the first line of the vcf
    :return: hopefully a nice csv file
    """

    vp = VcfParse(inputfile, samplefield)
    if not inputfile or not outputfile:
        print("""
            Hey you need to make sure to have both an inputfile and an outputfile! please use vcflat --help 
            to get more information
            """
              )
        exit()
    if isinstance(keys, str):
        keys = keys.split()
        print( f'using these keys :{keys}')
        vp.write2csv(outputfile, keys, sample)
    elif slowkeys:
        print("Since no keys were given, all keys need to be determined "
              "and they will all be spit out")
        keys = vp.get_header()
        print(f'using these keys :{keys}')
        vp.write2csv(outputfile, keys, sample)
    else:
        print("using the first row to determine column names, "
              "if you are missing something, use fastkeys=False")
        keys = vp.get_header_fast()

        print(f'using these keys :{keys}')
        vp.write2csv(outputfile, keys, sample)

if __name__ == '__main__':
    vcflat()