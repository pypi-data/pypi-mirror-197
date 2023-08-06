import sys
import csv
from openpyxl.cell.cell import ILLEGAL_CHARACTERS_RE

def main():

    writer = csv.writer(sys.stdout)

    for row in csv.reader(sys.stdin):
        for j, col in enumerate(row):
            row[j] = ILLEGAL_CHARACTERS_RE.sub("",col)
        writer.writerow(row)


if __name__ == "__main__":
    main()
