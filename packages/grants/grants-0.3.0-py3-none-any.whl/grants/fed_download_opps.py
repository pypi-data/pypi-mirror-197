# Copyright Kevin Lai <zlnh4@umsystem.edu>, Jan 2022

# Specifically, this file downloads the full opportunity webpage given the a url
# This script accepts a csv document from stdin. The csv is the same as the one
# retrieved from grants.gov. The output is the same document with 4 extra columns
# containing the html of the opportunity's general info, eligibility, additional info
# as HTML

"""
USAGE: python3 opportunity.py 
"""

from selenium import webdriver
import os
import time
import csv
import sys
from grants.fieldnames import *
from grants.fed_extract_attr import split_hyperlink

def main():
    os.environ["PATH"] += os.pathsep + os.path.dirname(os.path.abspath(__file__))
    writer = csv.writer(sys.stdout)
    for row in csv.reader(sys.stdin):
        url, id = split_hyperlink(row[0])

        options = webdriver.FirefoxOptions()
        options.headless = True
        
        while True:
            try:
                with webdriver.Firefox(
                    executable_path="geckodriver",
                    options=options,
                ) as driver:
        
                    print(f"Retrieving {id}", file=sys.stderr)
                    driver.get(url.replace("\"", "").strip())
                    try:
                        # Gives time to load. Otherwise, find_element_by_id will fail
                        time.sleep(1)
                        # The link we need to click is inside an iframe
                        driver.switch_to.frame("embeddedIframe")
                        left = driver.find_element("id","synopsisDetailsGeneralInfoTableLeft").get_attribute("innerHTML")
                        right = driver.find_element("id","synopsisDetailsGeneralInfoTableRight").get_attribute("innerHTML")
                        eligibility = driver.find_element("id","synopsisDetailsEligibilityTable").get_attribute("innerHTML")
                        additional_info = driver.find_element("id","synopsisDetailsAdditionalInfoTable").get_attribute("innerHTML")
                    except:
                        print("Failed", file=sys.stderr)
                        continue
                    
                    row[FED_LEFT_COLUMN_HTML] = left
                    row[FED_RIGHT_COLUMN_HTML] = right
                    row[FED_ELIGIBILITY_HTML] = eligibility
                    row[FED_ADDITIONAL_INFO_HTML] = additional_info
                    print(f"OK", file=sys.stderr)
                    
            except BlockingIOError:
                print("Blocking IO", file=sys.stderr)
                time.sleep(1)
                continue
            else:
                break
        writer.writerow(row)
            

if __name__ == "__main__":
    main()
