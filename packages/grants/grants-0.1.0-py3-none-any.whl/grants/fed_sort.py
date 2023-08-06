"""
USAGE: fed_sort ( title | agency | posted-date | amount | close-date  ) [ --reverse ]
"""
import docopt
import sys
import csv
from grants.fieldnames import *
import datetime

def sort_date(data):
    try:
        datetime.datetime.strptime(data, "%m/%d/%Y").timestamp()
    except:
        return 0

def main():
    args = docopt.docopt(__doc__)
    if args["title"]:
        sortfn = lambda x: x[FED_OPPORTUNITY_TITLE]
    elif args["agency"]:
        sortfn = lambda x: x[FED_AGENCY_NAME]
    elif args["posted-date"]:
        sortfn = lambda x: x[FED_POSTED_DATE]
    elif args["amount"]:
        sortfn = lambda x: x[FED_ESTIMATED_FUNDING]
    elif args["close-date"]:
        sortfn = lambda x: sort_date(x[FED_CLOSE_DATE])
    
    rows = list(csv.reader(sys.stdin))
    rows.sort(key=sortfn, reverse=args["--reverse"])
    csv.writer(sys.stdout).writerows(rows)
