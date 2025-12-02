import os
import sys
import gspread
from pathlib import Path
from string import Template
from google.oauth2.service_account import Credentials
from tqdm import tqdm
from dotenv import load_dotenv

from generater import generate_structured_json
from sender import create_post

load_dotenv()

SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")

SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]

creds = Credentials.from_service_account_file(
    "service-account.json",
    scopes=SCOPES
)

client = gspread.authorize(creds)


def main():
    if len(sys.argv) < 2:
        sheet_name = "Marketing AI"
    else:
        sheet_name = sys.argv[1]
    worksheet = client.open_by_key(SPREADSHEET_ID).worksheet(sheet_name)
    values = worksheet.get_all_values()

    template = Template(Path(__file__).with_name("prompt_template.txt").read_text(encoding="utf-8"))

    # row = values[1]

    # prompt = template.safe_substitute(
    #     AI_NAME=str(row[1]),
    #     AI_OFFICIAL_LINK=str(row[2]),
    #     PRICING_LINK=str(row[3]),
    #     DEMO_LINK=str(row[4]),
    # )
    # data = generate_structured_json(prompt)
    
    # create_post(data)

    for row in tqdm(values[1:], desc=f"Processing rows in {sheet_name}"):
        if row[1] != "":
            prompt = template.safe_substitute(
                AI_NAME=str(row[1]),
                AI_OFFICIAL_LINK=str(row[2]),
                PRICING_LINK=str(row[3]),
                DEMO_LINK=str(row[4]),
            )

            data = generate_structured_json(prompt)
        
            create_post(data)

if __name__ == "__main__":
    main()
