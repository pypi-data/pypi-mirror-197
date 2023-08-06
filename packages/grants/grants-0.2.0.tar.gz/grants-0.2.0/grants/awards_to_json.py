import json
import csv
import sys
import decimal
from decimal import Decimal

AWARD_MO_YR = 0
PI = 1
CO_PI = 2
SHARED_CREDIT = 3
DEPARTMENT = 4
CENTER = 5
PROPOSAL_TITLE = 6
SOURCE = 7
TYPE = 8
CFDA_NO = 9
ATTRIBUTES = 10
AGENCY = 11
TOTAL_PER_GRANT_AWARD = 12
TOTAL = 13
DIRECT = 14
INDIRECT = 15
DATE_AWARDED = 16
PROPOSAL_NUMBER = 17
PROJECT_NUMBER = 18
DEPARTMENT_AMOUNT = 19
CENTER_AMOUNT = 20
SUB = 21
SPEC = 22
FEDERAL_FUND_SOURCE = 23
IP_15 = 24


PROJECT_PROTOTYPE = {
    "project_number": int,
    "title": str,
    "total": int,
    "direct": int,
    "indirect": int,
}


PI_PROTOTYPE = {
    "name": str,
    "shared_credit": int,
    "department": str,
    "center": str,
    "is_primary": str,
}


PROPOSAL_PROTOTYPE = {
    "proposal_number": int,
    "award_date": str,
    "source": str,
    "cfda_no": str,
    "attributes": str, 
    "agency": str,
    "date_awarded": str,
    "federal_fund_source": str,
    "sub": str,
    "spec": str,
    "projects": list,
    "investigators": list,
}


def try_cast(value, type_obj):
    try:
        return type_obj(value)
    except ValueError:
        print(value, file=sys.stderr)
        return value
    except decimal.InvalidOperation:
        return value

def handle_decimal(value):
    return int(Decimal(value).quantize(Decimal("0.01"), decimal.ROUND_HALF_UP)) * 100



def main():
    last_proposal = ""
    last_project = ""

    proposals = []

    reader = csv.reader(sys.stdin)
    for row in reader:
        try:
            if int(row[PROPOSAL_NUMBER]) == 0:
                continue
        except ValueError:
            continue
        except IndexError:
            continue
        if row[PROPOSAL_NUMBER] != last_proposal:     
            last_proposal =  row[PROPOSAL_NUMBER]
            proposal = { k: PROPOSAL_PROTOTYPE[k]() for k in  PROPOSAL_PROTOTYPE }
            proposal["proposal_number"] = try_cast(row[PROPOSAL_NUMBER], int)
            proposal["source"] = row[SOURCE]
            proposal["cfda_no"] = row[CFDA_NO]
            proposal["attributes"] = row[ATTRIBUTES]
            proposal["agency"] = row[AGENCY]
            proposal["date_awarded"] = row[DATE_AWARDED]
            proposal["federal_fund_source"] = row[FEDERAL_FUND_SOURCE]
            proposal["sub"] = row[SUB]
            proposal["spec"] = row[SPEC]
            proposal["award_date"] = row[0]
            proposals.append(proposal)
            
        if row[PROJECT_NUMBER] != last_project:
            last_project = row[PROJECT_NUMBER]
            project = { k: PROJECT_PROTOTYPE[k]() for k in PROJECT_PROTOTYPE }
            project["title"] = row[PROPOSAL_TITLE]
            project["project_number"] = try_cast(row[PROJECT_NUMBER], int)
            project["total"] = try_cast(row[TOTAL], handle_decimal)
            project["indirect"] = try_cast(row[INDIRECT], handle_decimal)
            project["direct"] = try_cast(row[DIRECT], handle_decimal)
            proposals[-1]["projects"].append(project)
            
        

        investigator = { k: PI_PROTOTYPE[k]() for k in PI_PROTOTYPE }
        investigator["name"] = row[CO_PI]
        investigator["shared_credit"] = try_cast(row[SHARED_CREDIT], float)
        investigator["department"] = row[DEPARTMENT]
        investigator["center"] = row[CENTER]
        investigator["department_amount"] = try_cast(row[DEPARTMENT_AMOUNT], handle_decimal)
        investigator["center_amount"] = try_cast(row[CENTER_AMOUNT], handle_decimal)
        investigator["project"] = try_cast(row[PROJECT_NUMBER], int)
        investigator["is_primary"] = try_cast(row[PI], bool)

        proposals[-1]["investigators"].append(investigator) 
    print(json.dumps(proposals))
        




if __name__ == "__main__":
    main()
