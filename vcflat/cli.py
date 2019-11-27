from CsvOut import generatecsv
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
@click.option(
    '--slowkeys',
    help='keys for columns',
    is_flag=True

)
def vcfflat(inputfile,outputfile,sample,keys,slowkeys):
    fastkeys = True
    if slowkeys:
        fastkeys = False

    generatecsv(inputfile,
                outputfile,
                sample=sample,
                keys=keys,
                fastkeys=fastkeys)


if __name__ == '__main__':
    vcfflat()