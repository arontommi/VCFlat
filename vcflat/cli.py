import click

from vcflat.OutputHandle import OutputHandle, OutputPPrint

@click.command(context_settings={'help_option_names':['-h','--help']})
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
    '--keys',
    help='keys for columns, select columns to extract and use in the output file'
)
@click.option(
    '--slowkeys',
    help='if you just want to use all keys found in the vcf, else it uses only the ones in the first variant',
    is_flag=True,
    flag_value=True
)
@click.option(
    '--annotation',"-a",
    help='To avoid to many annotation columns and rows you can specify what annotation to use'
)
@click.option(
    '--long_anno',"-la",
    help='default is set at 20 "to handle large annotation events'
)

@click.option(
    '--pprint_header',
    help='prints the header of the vcf file',
    is_flag=True,
    flag_value=True
)

def vcflat(inputfile,pprint_header, outputfile=None, sample="Sample",keys=False, slowkeys=True, annotation=None, long_anno=None):
    if pprint_header:
        OutputPPrint(inputfile)
    else:
        OutputHandle(inputfile=inputfile,
                     outputfile=outputfile,
                     sample=sample,
                     keys=keys,
                     slowkeys=slowkeys,
                     annotation=annotation,
                     long_anno=long_anno)


if __name__ == '__main__':
    vcflat()
