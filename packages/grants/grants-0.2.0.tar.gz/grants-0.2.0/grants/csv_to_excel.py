"""
USAGE: csv_to_excel <csv> <excel> [ --header  ]
"""

import sys
import csv
import pandas as pd
import docopt

def main():
    args = docopt.docopt(__doc__)
    df = pd.read_csv(sys.argv[1], index_col=None)
    ex = pd.ExcelWriter(f'{sys.argv[2]}')
    df.to_excel(ex, header=args["--header"], index=False)
    ex.save()

if __name__ == "__main__":
    main()
