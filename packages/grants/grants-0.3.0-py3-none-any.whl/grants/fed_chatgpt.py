from revChatGPT.V1 import Chatbot
import sys
import os
import asyncio
import csv
import time
from grants.fieldnames import *


TOKEN = os.environ["OPENAI_TOKEN"]

PROMPT = """
We are a public, nonprofit, state controlled, research University in Missouri. We are an institute of
higher education. We are not a minority serving institution. We are not a 
women's college. We do not accept opportunities that serve countries other than the United States.
We are a United States entity.
We do not accept opportunities that mention countries other than the United States in the title.
We do not accept opportunities that mention states other than the state of Missouri in the title.
Given a funding description and eligibility, please respond
in YES or NO whether or not we are eligibile. If not enough information is given
say YES. Then on the next line, explain why.

The funding eligibility and description is in the following format

[TITLE]
Name of opportunity
[ELIGIBILITY]
Information on eligibility
[DESCRIPTION]
Funding description


"""

def create_prompt(title, eligibility, description):
    string = f"[Title]\n{title}\n[Eligibility]\n{eligibility}\n[Description]\n{description}\n"
    return PROMPT + string

def main():
    
    chatbot = Chatbot({"session_token":TOKEN, "paid": True})
    
    reader = csv.reader(sys.stdin)
    writer = csv.writer(sys.stdout)
    
    async def _main():
        
        for row in reader:
            title = row[FED_OPPORTUNITY_TITLE]
            eligibility = row[16]
            description = row[28]
            SELECT_INDEX = 29 
            
            while True:
                try:
                    result = ""
                    why = ""
                    response = list(chatbot.ask(create_prompt(title, eligibility, description)))
                     
                    message = response[-1]["message"]
                    result, why = message.split("\n")

                except:
                    print("ERROR", file=sys.stderr)
                    time.sleep(20)
                    continue
                else:
                    if "YES" in result:
                        select = "Add"
                    elif "NO" in result:
                        select = "Delete"
                    
                    row[SELECT_INDEX] = select
                    row.append(why)
                    writer.writerow(row)
                    time.sleep(20)
                    break
                    


    asyncio.run(_main())





if __name__ == "__main__":
    main()
