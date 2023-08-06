"""
Usage:
    fed_to_html < fed_grants.csv > fed_grants.html
"""

from extract_hyperlink import split_hyperlink
from fieldnames import *
import csv
import sys


ELEMENT_TEMPLATE = """
    <div class="element">
        <button class="Opportunity" onclick="opportunity(event)">
            <div class="OppLabel">{title}</div>
            <div class="OppLabel">{agency}</div>
            <div class="OppLabel">{amount}</div>
            <div class="OppLabel">{deadline}</div>
        </button>
        <div class="Details" style="display:none">
            <div class="label"><u>Eligibility</u></div>
            <div class="content">
                {eligibility}
            </div>
            <div class="label"><u>Description</u></div>
            <div class="content">
                {description}
            </div>
            <a href='{grants_url}'>See grants.gov Website</a>
        </div>
    </div>
"""

HTML_TEMPLATE = """
<!DOCTYPE HTML>
<html>
    <script>
        function opportunity(e)
        {{   
            let parent;
            if (e.target.tagName === "DIV")
                parent = e.target.parentNode.parentNode
            else if (e.target.tagName === "BUTTON")
                parent = e.target.parentNode
            
            let info = parent.children[1]
            let visible = info.getAttribute("style")

            if (visible === "display:none")
                info.setAttribute("style", "display:block")
            else if (visible === "display:block")
                info.setAttribute("style", "display:none")
        }}
    </script>
    <style>
        body {{
            padding:10px
        }}
        button {{
            width: 100%;
            margin:3x;
        }}

        .Details {{
            padding:10px;
            width: 100%;
            font-size: smaller;
        }}

        .OppLabel {{
            width:20%;
            display: inline-block;
            text-align: left;

        }}
        .label {{
            font-size: larger;
            font-weight: bold;
        }}

        .element {{
            border: 1px black;
            margin-top: 10px;
        }}

        .content {{
            font-size: medium
        }}
    </style>
<head>
</head>
<body>
    {elements}
</body>
</html>
"""

def main():
    
    reader = csv.reader(sys.stdin)
    elts = ""
    for row in reader:
        estimate, floor, ceil = row[FED_ESTIMATED_FUNDING], row[FED_AWARD_FLOOR], row[FED_AWARD_CEIL]
        if floor.strip() or ceil.strip():
            amount = f"{ceil} / {floor}"
        else:
            amount = f"{estimate}"

        
        elts += ELEMENT_TEMPLATE.format(
            title=row[FED_OPPORTUNITY_TITLE],
            agency=row[FED_AGENCY_NAME],
            amount=amount,
            deadline=row[FED_CLOSE_DATE],
            eligibility=row[FED_ELIGIBILITY_HTML],
            description=row[FED_ADDITIONAL_INFO_HTML],
            grants_url=split_hyperlink(row[0])[0]
        )
    print(HTML_TEMPLATE.format(elements=elts))
        
    
if __name__ == "__main__":
    main()
