from pancakevcf.VcfParse import *
import click

@click.command()
@click.option(
    '--inputfile', '-i',
    help='give it strelka a strelka file!',
)
@click.option(
    '--outputfile', '-o',
    help='give it outputfile!',
)
@click.option(
    '--sample', '-s',
    help='give it a sample',
)
@click.option(
    '--keys',
    help='keys for columns'
)

def main(inputfile,outputfile,sample):
    vp = VcfParse(inputfile, outputfile, sample, keys=False)
    vp.sample = sample
    df = vp.main_parse(input_vcf=inputfile)
    print(df.shape)