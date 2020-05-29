import sys

from vcflat.cli import vcflat as cli

"""
vcfflat.__main__
~~~~~~~~~~~~~~~~~~~~~
The main entry point for the command line interface.
Invoke as ``vcflat`` (if installed)
or ``python -m vcflat`` (no install required).
"""

if __name__ == "__main__":
    # exit using whatever exit code the CLI returned
    sys.exit(cli())
