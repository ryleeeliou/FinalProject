import random 

class Account: 
    def __init__(self, account_number, first_name, last_name, ssn, pin):
        self.account_number = account_number
        self.first_name = first_name
        self.last_name = last_name
        self.ssn = ssn
        self.pin = pin 
        self.balance = 0 #this will change, starting at 0
    
    #Getters and setters
    def get_account_number(self):
        return self.account_number
    
    def get_first_name(self):
        return self.first_name
    
    def set_first_name(self, first_name):
        self.first_name = first_name 
    
    def get_last_name(self):
        return self.last_name 
    
    def set_last_name(self, last_name):
        self.last_name = last_name

    def get_ssn(self):
        return self.ssn
    
    def set_ssn(self, ssn):
        self.ssn = ssn 

    def get_pin(self):
        return self.pin
    
    def set_pin(self, pin):
        self.pin = pin
    
    def get_balance(self):
        return self.balance
    
    def deposit(self, amount):
        self.balance += amount
        return self.balance 
    
    def withdraw(self, amount): #if sufficient funds subtract them, else -1
        if self.balance >= amount:
            self.balance -= amount
            return self.balance
        else:
            return -1 
        
    def is_valid_pin(self,pin):
        return self.pin == pin
    
    def __str__(self): # returns account info in form of string.
        return (f"---------------------------------------------\n"
                f"Account Number: {self.account_number}\n"
                f"Owner First Name: {self.first_name}\n"
                f"Owner Last Name: {self.last_name}\n"
                f"SSN: XXX-XX-{self.ssn[-4:]}\n" #only show last 4
                f"PIN: {self.pin}\n"
                f"Balance: ${self.balance / 100:.2f}\n" #.2f signifies two decimal places
                f"----------------------------------------------")

class Bank:
    max_accounts = 100 #for sake of simplicity and bounds of program

    def __init__(self):
        self.accounts = [None] * self.max_accounts

    def add_account_to_bank(self,account):
        for i in range(self.max_accounts):
            if self.accounts[i] is None:
                self.accounts[i] = account
                return True
        print("No more accounts available!")
        return False
    
    def remove_account_from_bank(self, account):
        for i in range(self.max_accounts):
            if self.accounts[i] and self.accounts[i].get_account_number() == account.get_account_number():
                self.accounts[i] = None
                return True
        return False 
    
    def find_account(self, account_number):
        for account in self.accounts:
            if account and account.get_account_number() == account_number:
                return account
        return None 
    
    def add_monthly_interest(self, annual_interest_rate):
        monthly_rate = annual_interest_rate / 12 / 100
        for account in self.accounts:
            if account:
                interest = account.get_balance() * monthly_rate
                account.deposit(int(interest))

class CoinCollector:
    @staticmethod
    def parse_change(change_str): #Helps to count change
        coin_values = {
            'P': 1, 'N': 5, 'D': 10, 'Q': 25, 'H': 50, 'W': 100
        }
        return sum(coin_values.get(coin, 0) for coin in change_str)
    
class BankUtility:
    @staticmethod
    def is_numeric(value): #will be used for prompts later where a number is required
        return value.isdigit()
    
    @staticmethod
    def prompt_user_for_string(prompt): #will be used later for prompts that require a string response
        return input(prompt)
    
    @staticmethod
    def prompt_user_for_positive_number(prompt):
        while True: #try/except to ensure positive number entered
            try:
                value = float(input(prompt))
                if value > 0:
                    return value 
                else:
                    print("Amount cannot be negative. Please try again.")
            except ValueError:
                print("Invalid input. Please enter a positive number.")

    @staticmethod
    def convert_from_dollars_to_cents(dollars):
        return int(dollars * 100)
    
    @staticmethod
    def generate_random_integer(min_value, max_value): #random values for account numbers and pin assignments 
        return random.randint(min_value, max_value)

#main module

class BankManager:
    def __init__(self):
        self.bank = Bank()

    def main(self):
        while True:
            print("------------------Bank-------------------")
            print("1: Open an account")
            print("2: Get account information and balance")
            print("3: Change PIN")
            print("4: Deposit money in account")
            print("5: Transfer money between accounts")
            print("6: Withdraw money from account")
            print("7: ATM withdrawal")
            print("8: Deposit change")
            print("9: Close an account")
            print("10: Add monthly interest to all accounts")
            print("11: Exit Program")
            print("-----------------------------------------")
           
            choice = input("Please enter a number from the options above: ")

            if choice == '1':
                self.open_account()
            
            elif choice == '2':
                self.get_account_info()

            elif choice == '3':
                self.change_pin()

            elif choice == '4':
                self.deposit_money()

            elif choice == '5':
                self.transfer_money()

            elif choice == '6':
                self.withdraw_money()

            elif choice == '7':
                self.atm_withdrawal()

            elif choice == '8':
                self.deposit_change()

            elif choice == '9':
                self.close_account()

            elif choice == '10':
                self.add_monthly_interest()
            
            elif choice == '11':
                print("Exiting Program...")
                break
            
            else:
                print("Invalid option. Please choose from the selection above.")

    # account info methods 

    def open_account(self):
        first_name = BankUtility.prompt_user_for_string("Enter Account Owner's First Name: ")
        last_name = BankUtility.prompt_user_for_string("Enter Account Owner's Last Name: ")
        ssn = BankUtility.prompt_user_for_string("Enter Account Owner's SSN (9 digits): ")

        while True:
            account_number = BankUtility.generate_random_integer(10000000, 99999999)
            if self.bank.find_account(account_number) is None:
                break

        pin = f"{BankUtility.generate_random_integer(0, 9999):04}"
        account = Account(account_number, first_name, last_name, ssn, pin)
        if self.bank.add_account_to_bank(account):
            print(account)

    def get_account_info(self):
        account = self.prompt_for_account_number_and_pin()
        if account:
            print(account)

    def change_pin(self):
        account = self.prompt_for_account_number_and_pin()
        if account:
            new_pin = BankUtility.prompt_user_for_string("Enter new PIN:")
            account.set_pin(new_pin)
            print("PIN changed successfully!")

    def deposit_money(self):
        account = self.prompt_for_account_number_and_pin()
        if account:
            amount = BankUtility.prompt_user_for_positive_number("Enter amount to deposit: ")
            account.deposit(BankUtility.convert_from_dollars_to_cents(amount))
            print(f"New Balance: ${account.get_balance() / 100:.2f}")

    def transfer_money(self):
        source_amount = self.prompt_for_account_number_and_pin()
        if source_amount:
            dest_account_number = BankUtility.prompt_user_for_string("Enter account number to transfer funds to: ")
            dest_account = self.bank.find_account(int(dest_account_number))
            if dest_account:
                amount = BankUtility.prompt_user_for_positive_number("Enter amount to transfer: ")
                amount_in_cents = BankUtility.convert_from_dollars_to_cents(amount)
                if source_amount.withdraw(amount_in_cents) != -1:
                    dest_account.deposit(amount_in_cents)
                    print("Transfer successful!")
                else:
                    print("Insufficient funds.")

            else:
                print("Destination account not found.")
    def withdraw_money(self):
        account = self.prompt_for_account_number_and_pin()
        if account:
            amount = BankUtility.prompt_user_for_positive_number("Enter amount to withdraw: ")
            if account.withdraw(BankUtility.convert_from_dollars_to_cents(amount)) != -1:
                print(f"New balance: ${account.get_balance() / 100:.2f}")
            else:
                print("Insufficient funds.")

    def atm_withdrawal(self):
        self.withdraw_money()

    def deposit_change(self):
        account = self.prompt_for_account_number_and_pin()
        if account:
            change_str = BankUtility.prompt_user_for_string("Enter change (P for penny, N for nickel, D for dime, etc.: )")
            amount = CoinCollector.parse_change(change_str)
            account.deposit(amount)
            print(f"New balance: ${account.get_balance() / 100:.2f}")

    def close_account(self):
        account = self.prompt_for_account_number_and_pin()
        if account:
            self.bank.remove_account_from_bank(account)
            print("Account closed!")
    
    def add_monthly_interest(self):
        rate = BankUtility.prompt_user_for_positive_number("Please enter annual interest rate (%): ")
        self.bank.add_monthly_interest(rate)
        print("Monthly interest added to all accounts!")

    def prompt_for_account_number_and_pin(self):
        account_number = BankUtility.prompt_user_for_string("Please enter account number: ")
        account = self.bank.find_account(int(account_number))
        if account:
            pin = BankUtility.prompt_user_for_string("Please enter PIN: ")
            if account.is_valid_pin(pin):
                return account
            else:
                print("Invalid PIN.")
                return None
            
        else:
            print(f"Account not found for account number {account_number}")
            return None
        
if __name__ == '__main__':
    manager = BankManager()
    manager.main()

        