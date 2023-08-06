"USAGE: piv_to_json <title>"
import sys
import csv
import json
import docopt
import datetime


from grants.fed_extract_attr import *
from grants.fieldnames import *


def main(): 
    args = docopt.docopt(__doc__)
    title = args["<title>"]
    rows = []
    for row in csv.reader(sys.stdin):
        url, id = split_hyperlink(row[0])
        rows.append({
            "id": id,
            "title": row[FED_OPPORTUNITY_TITLE],
            "agency": row[FED_AGENCY_NAME],
            "estimatedFunding": row[FED_ESTIMATED_FUNDING],
            "closeDate": row[FED_CLOSE_DATE],
            "amountFloor": row[FED_AWARD_FLOOR],
            "amountCeil": row[FED_AWARD_CEIL],
            "url": url,
            "description": row[FED_ADDITIONAL_INFO_HTML],
            "eligibility": row[FED_ELIGIBILITY_HTML],
        })

    print(json.dumps({
            "title": title,
            "data": rows,
            "updateTime": datetime.date.today().strftime("%m/%d/%Y")

    }))
