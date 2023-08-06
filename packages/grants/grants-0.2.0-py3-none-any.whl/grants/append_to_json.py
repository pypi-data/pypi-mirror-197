"""
USAGE: append_to_json <old> <new>
"""
import docopt
import json
import datetime

def main():
    args = docopt.docopt(__doc__)
    
    with open(args['<old>']) as fp:
        old = json.load(fp)

    with open(args['<new>']) as fp:
        new = json.load(fp)
    
    id_set = set(elt["id"] for elt in old["data"])
    
    # Verify new opps as actually new
    for elt in new["data"]:
        if elt["id"] not in id_set:
            elt["new"] = True
        else:
            elt["new"] = False

    still_valid = []

    # Delete old opps
    for elt in old["data"]:
        if not elt["closeDate"]:
            continue

        deadline = datetime.datetime.strptime(elt["closeDate"], "%m/%d/%Y")
        update_time = datetime.datetime.strptime(new["updateTime"], "%m/%d/%Y")
        if deadline >= update_time:
            still_valid.append(elt)

    still_valid.extend(new['data'])
    new["data"] = still_valid

    import sys
    json.dump(new, sys.stdout)
    

