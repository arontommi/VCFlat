import sys

from cli import vcfflat as cli

"""
vcfflat.__main__
~~~~~~~~~~~~~~~~~~~~~
The main entry point for the command line interface.
Invoke as ``vcfflat`` (if installed)
or ``python -m vcfflat`` (no install required).
"""

if __name__ == "__main__":
    # exit using whatever exit code the CLI returned
    sys.exit(cli())