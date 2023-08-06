"""
USAGE: fed_set ( intersection | union | difference ) <rvalue>
"""

import sys
import csv
import docopt
from grants.fed_extract_attr import split_hyperlink

def main():
    args = docopt.docopt(__doc__)
    writer = csv.writer(sys.stdout)
    lvalue = list(csv.reader(sys.stdin))

    with open(args["<rvalue>"]) as fp:
        rvalue = list(csv.reader(fp))
 
    rvalue_dict = {}
    for row in rvalue:
        try:
            id = split_hyperlink(row[0])[1]
        except:
            if "=HYPERLINK" not in row[0]:
                rvalue_dict[row[0]] = row
        else:
            rvalue_dict[id] = row

    lvalue_dict = {
        split_hyperlink(row[0])[1] : row
        for row in lvalue
    }
    
    lvalue_set = set(lvalue_dict)

    if args["intersection"]:
        intersection = lvalue_set.intersection(rvalue_dict)
        writer.writerows([ lvalue_dict[key] for key in intersection ])
    elif args["union"]:
        lvalue_dict.update(rvalue_dict)
        writer.writerows([ lvalue_dict[key] for key in lvalue_dict ])
    elif args["difference"]:
        diff = lvalue_set.difference(rvalue_dict)
        writer.writerows([ lvalue_dict[k] for k in diff ])
 

if __name__ == "__main__":
    main()
