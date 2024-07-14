import csv
from validate_email import validate_email
import re
import datetime
import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('diaspora_society')

balance = SHEET.worksheet('balance')

class Bank:

    def __init__(self):
        '''
        Create empty dictionary
        '''
        self.accounts = {}    # empty dictionary

    def create_account(self, account_number, account_user, joining_balance,
                       age, gender, pin, email):
        '''
        Create account user details and check if account exist already.
        '''               
        if account_number in self.accounts:
            return "Account already exists"
        if joining_balance < 400:
            return "Joining balance must be over 400 Euros"

        self.accounts[account_number] = [account_user, joining_balance, age,
                                         gender, pin, email]
