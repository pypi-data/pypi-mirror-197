import csv
import sys

from grants.fieldnames import *

def main():
    
    reader = csv.reader(sys.stdin)
    writer = csv.writer(sys.stdout)
    writer.writerow([  ]) # pandas strips first row
    writer.writerow([
        "Opportunity Number",
        "Opportunity Title",
        "Agency Code",
        "Agency",
        "Close Date",
        "Award Ceil",
        "Award Floor",
        "Expected Number of Awards",
        "Eligibility",
        "Description",
        "Selection"
        ])

    for i, row in enumerate(reader):
        writer.writerow([
            row[FED_OPPORTUNITY_NUMBER],
            row[FED_OPPORTUNITY_TITLE],
            row[FED_AGENCY_CODE],
            row[FED_AGENCY_NAME],
            row[FED_CLOSE_DATE],
            row[FED_AWARD_CEIL],
            row[FED_AWARD_FLOOR],
            row[FED_EXPECTED_NUMBER_OF_AWARDS],
            row[16], # Eligibility
            row[FED_DESCRIPTION],
            row[FED_SELECTION_STATUS]
        ])


if __name__ == "__main__":
    main()
