"""
USAGE: fed_select <file> [ --review ]
"""
import csv
from grants.fieldnames import *
from html.parser import HTMLParser
import io
import docopt


def split_hyperlink(hyperlink):
    # hyperlink looks like:
    # =HYPERLINK("<url>", "<id>")
    # So strip the =HYPERLINK and wrapped parentheses, and split on comma           
    result = hyperlink.replace("=HYPERLINK(", " ")[:-1].split(",")
    result[0] = result[0].strip()
    return result[0].replace("\"", ""), result[1].replace("\"", "") 
 

class ExtractDescription(HTMLParser):
    """
    Extract the description from the HTML. Depending on the tag, we print
    terminal control characters to change the color of the text.
    """

    def __init__(self):
        HTMLParser.__init__(self)
        self.io = io.StringIO()

        self.description = ""
        self.in_description = False
        self.stack = []

    def handle_starttag(self, tag, attrs):
        if self.in_description:
            if tag == "em":
                # Print terminal control character to change color
                print("\033[1;35m;", file=self.io, end="")
            elif tag == "strong":
                # Print terminal control character to emphasis
                print("\033[3;33m", file=self.io, end="")

    def handle_data(self, data):
        # Found the Description label, enter the description context
        if "Description:" in data:
            self.in_description = True
            return
        
        # Exit description context
        if "Link to Additional Information" in data:
            self.in_description = False
        
        # If we are in description, print the data
        if self.in_description:
            print(data, file=self.io, end="")

    def handle_endtag(self, tag):
        if self.in_description:
            if tag == "p": # Print a newline
                print("", file=self.io)
            # Reset terminal color
            print("\033[0m", file=self.io, end="")


class ExtractEligibility(HTMLParser):

    def __init__(self):
        super().__init__()
        self.handler = self.noop
        self.eligibility = ""
        self.additional_eligible = ""

    def noop(self, data):
        pass
    
    def handle_starttag(self, tag, data):
        if self.handler == self.set_eligibility and tag == "br":
            self.eligibility += "\n"
        elif self.handler == self.set_additional_eligible and tag == "br":
            self.additional_eligible += "\n"
    
    def set_eligibility(self, data):
        self.eligibility += data

    def set_additional_eligible(self, data):
        self.additional_eligible += data

    def handle_data(self, data: str) -> None:
        # Found the Eligibility label. Next data element will be the eligibility text
        if "Eligible Applicants" in data:
            self.handler = self.set_eligibility
        # Found the Additional Information on Eligibility label. Next data element will be the eligibility text
        elif "Additional Information on Eligibility:" in data:
            self.handler = self.set_additional_eligible
        else:
            self.handler(data)

    

def main():
    args = docopt.docopt(__doc__)


    with open(args["<file>"], 'r') as fp:
        all = rows = list(csv.reader(fp))
        n_rows = len(all)
    
    
    if args["--review"]:
        # Only select rows marked for review
        rows = []
        for row in all:
            if row[FED_SELECTION_STATUS] == "Review":
                rows.append(row)
        n_rows = len(rows)

    if not rows:
        print("No rows to process")
        return

    try:
        i = 0
        while True:
            row = rows[i]
            elig_parser = ExtractEligibility()
            desc_parser = ExtractDescription()
            print("\033[2J")
            elig_parser.feed(row[FED_ELIGIBILITY_HTML])
            desc_parser.feed(row[FED_ADDITIONAL_INFO_HTML])

            print("\033[1;32mEligibility\033[0m")
            if elig_parser.eligibility:
                print(elig_parser.eligibility, end="\n\n")
            elif row[FED_RESERVED_FIELD_4]:
                print(row[FED_RESERVED_FIELD_4], end="\n\n")
            print("\033[1;32mAdditional Eligibility Info\033[0m")
            print(elig_parser.additional_eligible, end="\n\n")

            print("\033[1;32mDescription\033[0m")
            print(elig_parser.additional_eligible, end="\n\n")

            descr = desc_parser.io.getvalue()
            if descr:
                print(desc_parser.io.getvalue())
            elif row[FED_DESCRIPTION]:
                print(row[FED_DESCRIPTION])

            print("\033[1;32mTitle\033[0m")
            print(row[FED_OPPORTUNITY_TITLE], end="\n\n")

            print("\033[1;32mAgency\033[0m")
            print(row[FED_AGENCY_NAME], end="\n\n")


            print("\033[1;32mgrants.gov\033[0m")
            print(split_hyperlink(row[0])[0])
            print("")
            
            if row[FED_SELECTION_STATUS] == "Add":
                print(f"{i+1} / {n_rows} : "" \033[1;32mAdd\033[0m")
            elif row[FED_SELECTION_STATUS] == "Delete":
                print(f"{i+1} / {n_rows} : ""\033[1;31mDelete\033[0m")
            elif row[FED_SELECTION_STATUS] == "Review":
                print(f"{i+1} / {n_rows} : ""\033[1;33mReview\033[0m")
            elif row[FED_SELECTION_STATUS] == "":
                print(f"{i+1} / {n_rows} : ""NULL")
            
            print("Press: (j) - Prev | (k) - Next | (a) - Add | (d) Delete | (r) - Review")    
            
            user_input = input()
            if user_input == "j": # Previous opportunity
                i = (i - 1) % n_rows
            elif user_input == "k":
                i = (i + 1) % n_rows # Next opportunity
            elif not user_input and row[FED_SELECTION_STATUS]:
                # Quickly skip an opportunity that has been marked
                i = (i + 1) % n_rows
            elif not user_input and not row[FED_SELECTION_STATUS]:
                # Don't skip an opportunity that has not been marked
                pass
            
            # These clauses automatically advance too the next opportunity
            # after marking
            elif user_input == "a":
                row[FED_SELECTION_STATUS] = "Add"
                i = (i + 1) % n_rows
            elif user_input == "d":
                row[FED_SELECTION_STATUS] = "Delete"
                i = (i + 1) % n_rows
            elif user_input == "r":
                row[FED_SELECTION_STATUS] = "Review"
                i = (i + 1) % n_rows
    finally:
        # Update our database file
        with open(args["<file>"], 'w') as fp:
            writer = csv.writer(fp)
            writer.writerows(all)

if __name__ == "__main__":
    main()
