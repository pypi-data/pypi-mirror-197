from html.parser import HTMLParser
from typing import *
import csv
import sys
import datetime
import time
from grants.fieldnames import *

class AmountData:
    amount = ""
    amount_upper = ""
    amount_note = ""

    def __init__(self, string:str) -> None:
        p1 = string.partition("Amount Upper:") 
        amount, part, right = p1
        if part:
            self.amount = amount.strip()
        else:
            right = amount

        p2 = right.partition("Amount Note:")
        amount, part, right = p2;
        if part:
            self.amount_upper = amount.strip()
            self.amount_note = right.strip()
        else:
            self.amount_upper = amount.strip()


def to_timestamp(string):
    return datetime.datetime.strptime(string, "%d %b %Y").timestamp()

def to_timeformat(string):
    dt = datetime.datetime.strptime(string, "%d %b %Y")
    return dt.strftime("%m/%d/%Y")


def extract_deadline(string):
    # Deadlines presented in multiple rows
    # DATE - Confirmed / sponsor
    # Date - Anticipated / sponsor
    deadlines = []
    lines = string.split("\r")
    for line in lines:
        left, part, right = line.partition("-")
        left = left.strip()
        # Only get the deadlines in the future
        try:
            if part and time.time() < to_timestamp(left):
                deadlines.append(left)
        except ValueError:
            pass

    if deadlines:
        return deadlines[0]
    else:
        return ""
            

class AmountHTML(HTMLParser):

    amount_string = ""
    note_string = ""

    def __init__(self):
        super().__init__()
        self.start = False
    
    def handle_starttag(self, data, attr):
        # Amount note may contain html tags
        if data != "span": # First tag may be <span>
            self.start = True


    def handle_data(self, data):
        # Extract everything except the "Amount Note"
        if not self.start:
            self.amount_string = data

    @staticmethod
    def process(html):
        if html.endswith("</span>"):
            html = "<span>" + html

class DescriptionHTML(HTMLParser):

    def __init__(self):
        super().__init__()
        self.text = ""

    def handle_data(self, data):
        self.text += data


def main():    
    reader = csv.reader(sys.stdin)
    writer = csv.writer(sys.stdout)
    
    for row in reader:
        # Extract Amount data
        amountstr = row[FED_RIGHT_COLUMN_HTML]
        amount_data = AmountData(amountstr)

        preprocess = lambda s: s.replace("USD", "").strip()

        row[FED_AWARD_FLOOR] = preprocess(amount_data.amount)
        row[FED_AWARD_CEIL] = preprocess(amount_data.amount_upper)
        if amount_data.amount_upper:
            row[FED_ESTIMATED_FUNDING] = preprocess(amount_data.amount_upper)
        elif amount_data.amount:
            row[FED_ESTIMATED_FUNDING] = preprocess(amount_data.amount)
        
        # Extract deadline
        deadline = extract_deadline(row[FED_LEFT_COLUMN_HTML])
        row[FED_CLOSE_DATE] = to_timeformat(deadline) if deadline else ""
        
        # Extract Description
        descr_parser = DescriptionHTML()
        descr_parser.feed(row[FED_ADDITIONAL_INFO_HTML])
        row[FED_DESCRIPTION] = descr_parser.text
        
        # Extract Eligibility
        elig_parser = DescriptionHTML()
        elig_parser.feed(row[FED_ELIGIBILITY_HTML])
        row[FED_RESERVED_FIELD_4] = elig_parser.text       
        writer.writerow(row)


if __name__ == "__main__":
    main()
