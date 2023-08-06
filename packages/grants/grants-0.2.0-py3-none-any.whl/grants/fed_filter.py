"""
USAGE:
    fed_filter posted-date [ --start=<date> ] [ --end=<date> ]
    fed_filter close-date  [ --start=<date> ] [ --end=<date> ]
    fed_filter amount      [ --low=<amount> ] [ --high=<amount> ]
    fed_filter agency-code <pattern> [ --exclude ]
    fed_filter agency      <pattern> [ --exclude ]
    fed_filter title       <pattern> [ --exclude ]
    fed_filter select      <pattern> [ --exclude ]
    fed_filter num-awards  <pattern> [ --exclude ]
    fed_filter eligibility <pattern> [ --exclude ]
"""
import docopt
import sys
import csv
from grants.fieldnames import *
import datetime
import re

def timestamp(date):
    try:
        result = datetime.datetime.strptime(date, "%m/%d/%Y").timestamp()
        return result
    except:
        return 0

def filter_date(data, start, end, index):
    if start is None and end is not None:
        end_date = timestamp(end)
        filterfn = lambda x: timestamp(x[index]) <= end_date
    elif start is not None and end is None:
        start_date = timestamp(start)
        filterfn = lambda x: timestamp(x[index]) >= start_date
    elif start is not None and end is not None:
        start_date = timestamp(start)
        end_date = timestamp(end)
        filterfn = lambda x: start_date <= timestamp(x[index]) <= end_date
    else:
        filterfn = lambda x: True

    return list(filter(filterfn, data))

def amount_to_int(x):

    new_str = ""
    for c in x:
        if (ord("0") <= ord(c) <= ord("9")):
            new_str += c
    return int(new_str) if new_str else 0

def filter_amount(data, low, high, index):
    
    if low is None and high is not None:
        high = int(high)
        filterfn = lambda x: amount_to_int(x[index]) <= high

    elif low is not None and high is None:
        low = int(low)
        filterfn = lambda x: amount_to_int(x[index]) >= low
    elif low is not None and high is not None:
        high = int(high)
        low = int(low)
        filterfn = lambda x: low <= amount_to_int(x[index]) <= high
    else:
        filterfn = lambda x: True

    return list(filter(filterfn, data))

def filter_regex(data, index, pattern, exclude=False):
    new_list = []
    expr = re.compile(pattern)
    for row in data:
        column = row[index]
        result = expr.findall(column)
        if not exclude and result: 
            new_list.append(row)
        elif exclude and not result:
            new_list.append(row)

    return new_list

def main():
    args = docopt.docopt(__doc__)
    writer = csv.writer(sys.stdout)
    rows = list(csv.reader(sys.stdin))
    if args["posted-date"]:
        writer.writerows(filter_date(rows, args["--start"], args["--end"], FED_POSTED_DATE))
    elif args["close-date"]:
        writer.writerows(filter_date(rows, args["--start"], args["--end"], FED_CLOSE_DATE))
    elif args["agency-code"]:
        writer.writerows(filter_regex(rows, FED_AGENCY_CODE, args["<pattern>"], args["--exclude"]))
    elif args["agency"]:
        writer.writerows(filter_regex(rows, FED_AGENCY_NAME, args["<pattern>"], args["--exclude"]))
    elif args["title"]:
        writer.writerows(filter_regex(rows, FED_OPPORTUNITY_TITLE, args["<pattern>"], args["--exclude"]))
    elif args["select"]:
        writer.writerows(filter_regex(rows, FED_SELECTION_STATUS, args["<pattern>"], args["--exclude"]))
    elif args["num-awards"]:
        writer.writerows(filter_regex(rows, FED_EXPECTED_NUMBER_OF_AWARDS, args["<pattern>"], args["--exclude"]))

    elif args["amount"]:
        writer.writerows(filter_amount(rows, args["--low"], args["--high"], FED_ESTIMATED_FUNDING))
    elif args["eligibility"]:
        writer.writerows(filter_regex(rows,FED_ELIGIBILITY, args["<pattern>"], args["--exclude"])) 
