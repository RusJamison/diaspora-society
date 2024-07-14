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
        field_names = ['account_number', 'account_user', 'joining_balance',
                       'age', 'gender', 'pin', 'email']
    
    def deposit(self, account_number, amount):
        '''
        Function to check account and deposit minimum of 50 euros
        '''
        if account_number not in self.accounts:
            return "Account does not exist"
        if amount <= 50:
            return "Amount to deposit must be over 50 Euros"
        #  [account_user, joining_balance, age, gender, pin, email]
        self.accounts[account_number][1] += amount
        return "Deposited " + str(amount)
        + " successfully. New balance : "
        + str(self.accounts[account_number][1])
    
    def withdraw(self, account_number, amount):
        '''
        Function to withdraw and update balance
        '''
        if account_number not in self.accounts:
            return "Account does not exist"
        if amount <= 50:
            return "Amount to withdraw must be over 50 Euros"

        if self.accounts[account_number][1] < amount:
            return "Insufficient balance."

        self.accounts[account_number][1] -= amount
        return "Withdrew " + str(amount)
        + " successfully. New balance : "
        + str(self.accounts[account_number][1])
    
    def check_balance(self, account_number):
        '''
        Function to check individual balance
        '''
        if account_number not in self.accounts:
            return "Account does not exist"

        return "Account User : " + self.accounts[account_number][0]
        + "\nBalance : " + str(self.accounts[account_number][1])
    
    def delete_account(self, del_acc_no):
        '''
        Function discontinue account
        '''
        if del_acc_no not in self.accounts:
            return "Account does not exist"
        if del_acc_no in self.accounts:
            self.accounts.pop(del_acc_no)
            return "deleted account  successfully"
    
    def edit_account(self, account_number, new_name):
        '''
        Function to change name i.e married name for a woman
        '''
        if account_number not in self.accounts:
            return "Account does not exist"
        if account_number in self.accounts:
            print("\nName before update "
                  + str(self.accounts[account_number][0]))
        self.accounts[account_number][0] = new_name

        return "Name changed successfully update name: " + str(
           self.accounts[account_number][0])
    
    def check_details(self, account_number):
        '''
        Checking account details
        '''
        if account_number not in self.accounts:

            return "Account does not exist"
        # [account_user0, joining_balance1, age2, gender3, pin4, email5]
        return "Account User : " + self.accounts[account_number][0]
        +"\nGender : " + self.accounts[account_number][3]
        +"\nAge : " + str(self.accounts[account_number][2])
        +"\nemail_id : " + self.accounts[account_number][5]
    
    def data_validation(self, account_number):
        '''
        Check pin
        '''
        if account_number not in self.accounts:
            return "Account does not exist"
        pin = input('Enter pin : ')
        if pin == self.accounts[account_number][4]:
            return True
        else:
            return False
    
    def transfer_funds(self, account_number, to_accnumber, amount):
        '''
        Function to transfer funds among users
        '''
        if account_number in self.accounts and to_accnumber in self.accounts:
            if self.accounts[account_number][1] >= amount:
                self.accounts[to_accnumber][1] += amount
                self.accounts[account_number][1] -= amount
                print("Transfer completed successfully.")
                return "Deposited " + str(amount)
                + " successfully. New balance : "
                + str(self.accounts[to_accnumber][1])
            else:
                print("Insufficient funds.")
        else:
            print("One or both accounts not found.")

bank = Bank()  # Create a Bank object
#def show_main_menu():
print("\nMENU OPTION")
print("1. Create Account")
print("2. Deposit Money")
print("3. Withdraw Money")
print("4. Check Balance")
print("5. Delete Account")
print("6. Edit  Account")
print("7. Display Account ")
print("8: Transfer Fund")
print("9. Display all accounts ")
print("10.Exit")
