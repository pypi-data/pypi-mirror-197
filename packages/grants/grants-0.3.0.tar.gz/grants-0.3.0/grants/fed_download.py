# Copyright Kevin Lai <zlnh4@umsystem.edu>, Jan 2022
# Download Federal Fund Opportunities for public institutions and state controlled institutions
"""
USAGE: downloader.py [--save=<file>]
"""

import glob
from selenium import webdriver
import os.path as fs
import os
import time
import csv
import docopt
import sys
from grants.fieldnames import FED_NUM_FIELDS

ELIGEABLE_PUBLIC_AND_STATE_CHECKBOX_ID = "06"
ELIGEABLE_OTHERS_ID = "25"
ELIGEABLE_UNRESTRICTED_ID = "99"

def main():

    args = docopt.docopt(__doc__)
    os.environ["PATH"] += os.pathsep + os.path.dirname(os.path.abspath(__file__))
    options = webdriver.FirefoxOptions()
    options.headless = True
    profile = webdriver.FirefoxProfile()

    # 2 tells preference to use none-default folder
    profile.set_preference("browser.download.folderList", 2)
    # which is we set as this folder
    profile.set_preference("browser.download.dir", fs.abspath(os.getcwd()))
    # Don't ask if we want to view or save the file. Automatically download to this folder
    profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "text/csv")


    with webdriver.Firefox(profile,
        executable_path="geckodriver",
        options=options,
    ) as driver:
        driver.get("https://www.grants.gov/web/grants/search-grants.html")


        # The link we need to click is inside an iframe
        
        try:
            driver.switch_to.frame("embeddedIframe")
        except:
            print("Embedded Iframe Error: try running this program again", file=sys.stderr)
            return

        # Set Search Criteria
        # 1) Uncheck Forecasted as it is checked by default.
        #  We only want Posted Grants which we do not need to click
        driver.find_element("id","forecasted").click()
        print("Unchecked Forecasted", file=sys.stderr)
        time.sleep(0.5)
        
        # 2) Select Public and state controlled institutions and Other
        driver.find_element("id",ELIGEABLE_PUBLIC_AND_STATE_CHECKBOX_ID).click()
        print("Selected Public and State Controlled Institutions", file=sys.stderr)
        time.sleep(0.5)
        driver.find_element("id",ELIGEABLE_OTHERS_ID).click()
        print("Selected Other", file=sys.stderr)
        driver.find_element("id", ELIGEABLE_UNRESTRICTED_ID).click()
        print("Selected 'Unrestricted'", file=sys.stderr)
        cur_csv = set(glob.glob("*.csv"))

        # Sometimes the download doesn't work, so try until it works.    
        while len(cur_csv) == len(result := set(glob.glob("*.csv"))):
            # Click the link
            driver.find_element("xpath","//a[@title='Click to export detailed data']").click()
            time.sleep(1)

        # Get the set of elements in result but not in cur_csv. This is the new csv file
        file = result.difference(cur_csv).pop()
        
        with open(file) as orig:
            reader = csv.reader(orig, dialect="excel")
            next(reader)

            # Set number of columns to FED_COLUMN_LENGTH. The number of fields
            # per row sometimes sometimes differ
            rows = []
            for data in reader:
               
                if data:
                    rowcopy = ["" for _ in range(FED_NUM_FIELDS) ]
                    for j, col in enumerate(data):
                        if j < FED_NUM_FIELDS:
                            rowcopy[j] = col.strip("\n")
                    rows.append(rowcopy)

            # Save the file if the user specified --save
            if args["--save"] is not None:
                with open(args["--save"], "w") as copy:
                    writer = csv.writer(copy)
                    writer.writerows(rows)
            # Otherwise just print the file to stdout and let another program handle
            # the output
            else:
                writer = csv.writer(sys.stdout)
                writer.writerows(rows)

        # Cleanup the tmp file
        os.remove(file)

if __name__ == "__main__":
    main()
