"""
USAGE: excel_to_csv <filename> <output>

Given excel file, print a csv file
"""
import pandas as pd
import docopt
import sys
import csv
import io
import os

def main():
    args = docopt.docopt(__doc__)
    excel = pd.ExcelFile(args["<filename>"])

    for sheet in excel.sheet_names:
        with open(f"{args['<output>']}-{sheet}.csv", "w") as fp:
            writer = csv.writer(fp)
            with io.StringIO() as buf:
                df = excel.parse(sheet)
                buf.write(df.to_csv())
                buf.seek(0, io.SEEK_SET)
                reader = csv.reader(buf)
                for row in reader:
                    del row[0] # Delete column inserted by pandas
                    writer.writerow(row)

