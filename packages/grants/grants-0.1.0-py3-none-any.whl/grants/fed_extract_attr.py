from html.parser import HTMLParser
from fieldnames import *
import csv
import sys

class AmountParser(HTMLParser):
    amount_ceil = ""
    amount_floor = ""
    total_funding = ""

    def __init__(self):
        super().__init__()
        self.handler = self.do_nothing

    def set_award_ceil(self, data):
        self.amount_ceil = data
        self.handler = self.do_nothing

    def set_award_floor(self, data):
        self.amount_floor = data
        self.handler = self.do_nothing
    
    def set_total_funding(self, data):
        self.total_funding = data
        self.handler = self.do_nothing

    def do_nothing(self, data):
        pass

    def handle_data(self, data):
        if data == "Award Ceiling:":
            self.handler = self.set_award_ceil
        elif data == "Award Floor:":
            self.handler = self.set_award_floor
        elif data == "Estimated Total Program Funding:":
            self.handler = self.set_total_funding
        else:
            self.handler(data)


def split_hyperlink(hyperlink):
    # hyperlink looks like:
    # =HYPERLINK("<url>", "<id>")
    # So strip the =HYPERLINK and wrapped parentheses, and split on comma           
    result = hyperlink.replace("=HYPERLINK(", " ")[:-1].split(",")
    result[0] = result[0].strip()
    return result[0].replace("\"", ""), result[1].replace("\"", "") 


def main():
    reader = csv.reader(sys.stdin)
    writer = csv.writer(sys.stdout)
    for row in reader:
        parser = AmountParser()
        right_col = row[FED_RIGHT_COLUMN_HTML]
        parser.feed(right_col)
        row[FED_AWARD_CEIL] = parser.amount_ceil
        row[FED_AWARD_FLOOR] = parser.amount_floor
        writer.writerow(row)



if __name__ == "__main__":
    main()