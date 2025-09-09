# CLI - i put a command "salary 8000"
# takes it and processes what type it is
# add the entry to the json database
# show remainings 

import json
from google import genai
from dotenv import load_dotenv
from pydantic import BaseModel
from google.genai import types

used_model = "gemini-2.0-flash"

load_dotenv()
client = genai.Client()
chat = client.chats.create(model=used_model)

with open("finman.json", 'r') as file:
        # Load existing data into a dictionary
        acct_info = json.load(file)


def add_data(entry: dict):
    global acct_info  # we’ll modify the global variable
    if "account_dets" not in acct_info:
        acct_info["account_dets"] = [entry]
    else:
        acct_info["account_dets"].append(entry)

    # Save back to file
    with open("finman.json", "w") as f:
        json.dump(acct_info, f, indent=3)


def show_income(data):
    for entry in data["account_dets"]:
        if entry["transaction_type"] == "income":
            print(f"{entry['category']} ----- {entry['amount']}")

def show_expense(data):
    for entry in data["account_dets"]:
        if entry["transaction_type"] == "expense":
            print(f"{entry['category']} ----- {entry['amount']}")
        

def show_balance(data):
    # Open and read the JSON file
    total_expense = 0
    total_income = 0
    #print(data["account_dets"][0]["amount"])

    for entry in data["account_dets"]:
        if entry["transaction_type"] == "income":
            total_income = total_income + entry["amount"] 
        elif entry["transaction_type"] == "expense":
            total_expense = total_expense + entry["amount"]

    balance = total_income - total_expense

    # print(f"Total Income: {total_income}")
    # print(f"Total Expense: {total_expense}")
    print(f"Balance: {balance}")
    return balance
# def add_data(file_data, entry): 
#     if "account_dets" not in file_data:
#         file_data["account_dets"] = [entry]
#     else:
#         file_data["account_dets"].append(entry)
    
#     # Move the cursor to the beginning of the file
#     file.seek(0)
    
#     # Write the updated data back to the file
#     json.dump(file_data, file, indent=3)


class Entry(BaseModel):
        command: str
        type: str
        category: str
        amount: int
        message: str        

def process_chat(user_message: str) -> dict:
    """
    Wraps your chat loop into a reusable function.
    Returns a dict the API can send directly to the frontend.
    """

    response = client.models.generate_content(
        model=used_model,
        contents=chat.send_message(user_message),
        config=genai.types.GenerateContentConfig(
            system_instruction=(
                f""" "You are an intelligent tracker and finance management app. Given any entry, you would "
                "1. Decide on the type of entry - income/ expense and set it in the 'fin_type'. "
                "2. If the type is income, select a category from - salary, loan_repaid. "
                "3. If the type is expense, select a category from - food, travel, family(spent on family members for any resources), "
                "friends(spent to buy anything for friends), utils (bought anything of daily necessity), myself (bought something entirely for the user). "
                "4. In 'amount' write the amount of money entried. No need for currency. If there is a k, remove k and multiply with 1000. "
                "5. If there is any ambiguity in the type of entry, make sure to ask the user for clarification. "
                "Set the 'command' as clarification and write your question in 'message'. "
                "If the ambiguity is cleared then respond as usual with 'command' as data and filling info in the structured form. "
                "6. If no ambiguity, set 'command' as data and respond with the info. For data type 'command' set message as 'entry added'. "
                "7. If the user asks for /report or anything of this sort, set 'command' as report "
                f"and write a report/insight with data from {json.dumps(acct_info, indent=3)} for the user in 'message'."
            """),
            response_mime_type="application/json",
            response_schema=Entry
        )
    )

    # Parse model response
    response_dict: dict = json.loads(response.text)

    # Handle each command type
    if response_dict["command"] == "clarification":
        return {"type": "clarification", "message": response_dict["message"]}

    elif response_dict["command"] == "report":
        return {"type": "report", "message": response_dict["message"]}

    elif response_dict["command"] == "data":
        acct_entry = {
            "transaction_type": response_dict["type"],
            "category": response_dict["category"],
            "amount": response_dict["amount"]
        }
        add_data(acct_entry)
        # Calculate new balance after adding entry
        balance = show_balance(acct_info)
        return {"type": "data", "message": "Entry added", "entry": acct_entry, "balance": balance}

    else:
        return {"type": "error", "message": "undefined format"}
