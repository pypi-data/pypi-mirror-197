"""
USAGE: piv_to_excel [--header]
"""
import csv
import sys
from grants.fieldnames import *
import docopt

def main():
    args = docopt.docopt(__doc__)
    
    writer = csv.writer(sys.stdout)
    reader = csv.reader(sys.stdin)
    
    writer.writerow([]) # Pandas likes to strip the first row
    if args["--header"]:
        writer.writerow([
            "Opportunity Number",
            "Title",
            "Funder",
            "Deadline",
            "All Deadlines",
            "Amount",
            "Eligibility",
            "Abstract",
            "Pivot URL",
            "Select"
            ])
    
    for row in reader:
        writer.writerow([
            row[FED_OPPORTUNITY_NUMBER],
            row[FED_OPPORTUNITY_TITLE],
            row[FED_AGENCY_NAME],
            row[FED_CLOSE_DATE],
            row[FED_LEFT_COLUMN_HTML],
            row[FED_ESTIMATED_FUNDING],
            row[FED_RESERVED_FIELD_4],
            row[FED_DESCRIPTION],
            row[FED_PIV_FUNDER_URL],
            row[FED_SELECTION_STATUS]
        ])

if __name__ == "__main__":
    main()
