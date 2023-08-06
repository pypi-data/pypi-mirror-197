"""
USAGE: toml_to_csv
"""

import csv
import sys
import toml
import docopt

from grants import fieldnames as fn

def main():
    args = docopt.docopt(__doc__)

    data = toml.load(sys.stdin)
    
    writer = csv.writer(sys.stdout)
    row = [ "" for _ in range(len(fn.FED_NUM_FIELDS ))  ]

    number = data["Opportunity Number"]["value"]
    url = data.get("URL", {}).get("value", "")

    row[fn.FED_OPPORTUNITY_NUMBER] = f'=HYPERLINK("{number}", "{url}")'
    row[fn.FED_OPPORTUNITY]

if __name__ == "__main__":
    main()
