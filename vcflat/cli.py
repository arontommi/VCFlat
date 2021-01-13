import click
import sys

from vcflat.OutputHandle import OutputHandle, OutputPPrint, OutputPPrintBodyHeader


@click.command(context_settings={'help_option_names':['-h','--help']},no_args_is_help=True)
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
    "--samples_in_header",
    help='To rename samples in the vcf body header, example: --samples_in_header "Tumor Normal"'
)
@click.option(
    '--pprint_header',
    help='prints the header of the vcf file',
    is_flag=True,
    flag_value=True
)
@click.option(
    '--pprint_body_header',
    help='prints the header of the vcf body',
    is_flag=True,
    flag_value=True
)
def vcflat(inputfile, pprint_header, pprint_body_header,
           outputfile=None, sample="Sample", keys=False, slowkeys=True,
           annotation=None, long_anno=None, samples_in_header=None):
    if pprint_header:
        OutputPPrint(inputfile)
    if pprint_body_header:
        OutputPPrintBodyHeader(inputfile)
    if not pprint_body_header and not pprint_header:
        OutputHandle(inputfile=inputfile,
                     outputfile=outputfile,
                     sample=sample,
                     keys=keys,
                     slowkeys=slowkeys,
                     annotation=annotation,
                     long_anno=long_anno,
                     samples_in_header=samples_in_header)


if __name__ == '__main__':
    vcflat()
