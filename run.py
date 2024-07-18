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
        with open('bank.csv', 'a')as csvfile:
            writer = csv.DictWriter(csvfile, field_names)
            # writer.writeheader()
            writer.writerow({'account_number': account_number,
                             'account_user': account_user,
                             'joining_balance': joining_balance,
                             'age': age,
                             'gender': gender,
                             'pin': pin,
                             'email': email})
        return "Account created successfully"

    def deposit(self, account_number, amount):
        '''
        Function to check account and deposit minimum of 50 euros
        [account_user, initial_balance, age, gender, pin, email]
        '''
        if account_number not in self.accounts:
            return "Account does not exist"
        if amount <= 50:
            return "Amount to deposit must be over 50 Euros"
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

        account_user = self.accounts[account_number][0]
        balance = self.accounts[account_number][1]
        return f"Account User: {account_user}\nBalance: {balance}"

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

        account_user = self.accounts[account_number][0]
        gender = self.accounts[account_number][3]
        age = self.accounts[account_number][2]
        email = self.accounts[account_number][5]

        return (
            f"Account User: {account_user}\n"
            f"Gender: {gender}\n"
            f"Age: {age}\n"
            f"Email ID: {email}"
        )

    def data_validation(self, account_number):
        '''
        Check pin
        '''
        if account_number not in self.accounts:
            return "Account does not exist"
        pin = input('Enter pin : \n')
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


def show_main_menu():
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


while True:
    show_main_menu()
    choice = input("\nEnter your Choice (1 to 10):\n")
    if choice == '1':
        count = 1
        while (count <= 3):
            account_number = input("Enter 7 digit Account Number :\n")
            acc = re.fullmatch('[0-9][0-9][0-9][0-9][0-9][0-9][0-9]',
                               account_number)
            if acc is not None:  # checked the number is valid  or not
                break
            print('Invalid account number it should be 7 digits! you'
                  'will getmax 3 attempt your ', count, 'attempt failed')
            count += 1
        if count == 4:
            break
        count = 1
        while (count <= 3):
            account_user = input("Enter Account User's Name :\n")
            a = account_user.strip()
            a = a.replace(" ", "").isalpha()
            if a is True:
                break
            print('Name must contain only alphabets reenter You will get'
                  'max 3 attempt your ', count, 'attempt failed')
            count += 1
            if count == 4:
                break
        count = 1
        while (count <= 3):
            age = input('Enter age :\n')
            if int(age) >= 18:
                break
            print('your age below 18  you cannot open account reenter'
                  'You will get max 3 attempt your', count, 'attempt failed')
            count += 1
            if count == 4:
                break

        gender = input('Enter Gender M for Male and F for Female :\n')
        joining_balance = float(input("Enter Joining Balance minimum 400 :\n"))
        count = 1
        while (count <= 3):
            pin = input("Enter 4 digit pin password :\n")
            a = re.fullmatch('[0-9][0-9][0-9][0-9]', pin)
            if a is not None:
                break
            print('This is not a valid pin must contain only 4 digits reenter'
                  'You will get max 3 attempt your ', count, 'attempt failed')
            count += 1
            if count == 4:
                break
        count = 1
        while (count <= 3):
            email = input('Enter email_id :\n')
            is_valid = validate_email(email)
            if is_valid is False:
                print("Invalid email addressreenter You will get max 3 attempt"
                      "your ',count ,'attempt failed")
            count += 1
            if count == 4:
                break
            else:
                result = bank.create_account(account_number, account_user,
                                             joining_balance, age, gender,
                                             pin, email)
            print(result)
            break

    elif choice == '2':
        account_number = input("Enter Account Number :\n")
        r = bank.data_validation(account_number)
        if r is False:
            print('Incoreect pin u cannot deposit')
            break
        amount = float(input("Enter Amount to Deposit :\n"))
        result = bank.deposit(account_number, amount)
        print(result)
        print(datetime.datetime.now())

    elif choice == '3':
        account_number = input("Enter Account Number :\n")
        r = bank.data_validation(account_number)
        if r is False:
            print('Incorrect account-number you cannot withdraw')
            break
        amount = float(input("Enter Amount to Withdraw :\n"))
        result = bank.withdraw(account_number, amount)
        print(result)
        print(datetime.datetime.now())

    elif choice == '4':
        account_number = input("Enter Account Number :\n")
        r = bank.data_validation(account_number)
        if r is False:
            print('Incorrect pin u cannot check balance')
            break
        result = bank.check_balance(account_number)
        print(result)

    elif choice == '5':
        account_number = input("Enter Account Number :\n")
        r = bank.data_validation(account_number)
        if r is False:
            print('Incorrect pin you cannot delete')
            break
        del_acc_no = input("Enter Account Number which you want to delete :\n")
        result = bank.delete_account(del_acc_no)
        print(result)
        print(datetime.datetime.now())

    elif choice == '6':
        account_number = input("Enter Account Number you want to edit :\n")
        r = bank.data_validation(account_number)
        if r is True:
            new_name = input('Enter new name :\n')
            a = new_name.strip()
            a = new_name.replace(" ", "").isalpha()
            if a is not True:
                print('Name must contain only alphabets')
                break
            result = bank.edit_account(account_number, new_name)
            print(result)
            print(datetime.datetime.now())
        else:
            print('Your enter wrong pin hence not allow to edit')

    elif choice == '7':
        account_number = input("Enter Account Number  to check details :\n")
        result = bank.check_details(account_number)
        print(result)

    elif choice == '8':
        account_number = input("Enter Account Number  :\n")
        r = bank.data_validation(account_number)
        if r is True:
            amount = float(input('Enter transfer amount :\n'))
            to_accnumber = input("Enter Account Number to Transfer fund  :\n")
            result = bank.transfer_funds(account_number, to_accnumber, amount)
            print(result)
            print(datetime.datetime.now())
    elif choice == '9':
        with open('bank.csv', mode='r') as file:
            csvFile = csv.reader(file)
            for lines in csvFile:
                if (lines != []):
                    print(lines)
    elif choice == '10':
        print("Exiting the program.")
        break
    else:
        print("Invalid Choice. Please Try Again !!!")
