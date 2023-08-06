"""
USAGE: piv_to_fed [--header]

Convert pivot-p csv to grants.gov csv
If --header flag is specified, strip the first row
"""
from grants.fieldnames import *
import sys
import csv
import docopt

def main():
    args = docopt.docopt(__doc__)
    
    reader = csv.reader(sys.stdin, dialect="excel")
    writer = csv.writer(sys.stdout)
    
    if args["--header"]:
        next(reader) # Strip header

    as_fed = []
    for line in reader:
        if line:
            row = [ "" for _ in range(FED_NUM_FIELDS)]
            row[FED_OPPORTUNITY_NUMBER] = f'=HYPERLINK("{line[PIV_FUNDER_URL]}", "{line[PIV_OPPORTUNITY_ID]}")'
            row[FED_OPPORTUNITY_TITLE] = line[PIV_TITLE]
            row[FED_AGENCY_CODE] = ""
            row[FED_AGENCY_NAME] = line[PIV_FUNDER]
            
            # Pivot-RP format is not normalized for deadlines.
            # There are multiple deadlines per opportunity so we
            # some further processing before transforming the pivot deadline
            # to the closing date
            row[FED_LEFT_COLUMN_HTML] = line[PIV_DEADLINE]
            
            # Pivot also has an upper/lower
            row[FED_RIGHT_COLUMN_HTML] = line[PIV_AMOUNT]
            row[FED_ELIGIBILITY_HTML] = line[PIV_ELIGIBILITY]
            row[FED_ADDITIONAL_INFO_HTML] = line[PIV_ABSTRACT]
            row[FED_PIV_FUNDER_URL] = line[PIV_FUNDER_URL]
            
            as_fed.append(row)

    writer.writerows(as_fed)

if __name__ == "__main__":
    main()
