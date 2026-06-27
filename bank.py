# http://localhost:8000
import json
import random
import string
from pathlib import Path
from datetime import datetime


class Bank:
    database = 'data.json'
    data = []
    AMOUNT_LIMIT = 500000

    @staticmethod
    def load_data():
        try:
            if Path(Bank.database).exists() and Path(Bank.database).stat().st_size > 0:
                with open(Bank.database) as fs:
                    Bank.data = json.load(fs)
            else:
                Bank.data = []
                Bank.save()
        except (json.JSONDecodeError, IOError):
            Bank.data = []
            Bank.save()

    @staticmethod
    def save():
        with open(Bank.database, 'w') as fs:
            json.dump(Bank.data, fs, indent=4)

    @staticmethod
    def generate_account():
        """Generate a professional-looking account number with date and sequence"""
        date_str = datetime.now().strftime("%Y%m%d")
        sequence = str(len(Bank.data) + 1).zfill(6)
        return f"BANK{date_str}{sequence}"

    def create_account(self, name, age, email, pin):
        if age < 18 or len(str(pin)) != 6:
            return "Invalid age or PIN"

        account = {
            "name": name,
            "age": age,
            "E-mail": email,
            "Pin": pin,
            "AccountNo": self.generate_account(),
            "Balance": 0,
            "CreatedAt": datetime.now().isoformat(),
            "Transactions": [
                {
                    "Type": "Account Created",
                    "Amount": 0,
                    "Balance": 0,
                    "Timestamp": datetime.now().isoformat(),
                    "Description": "New account created"
                }
            ]
        }

        Bank.data.append(account)
        Bank.save()
        return account

    def find_user(self, acc, pin):
        for user in Bank.data:
            if user["AccountNo"] == acc and user["Pin"] == pin:
                return user
        return None

    def deposit(self, acc, pin, amount):
        user = self.find_user(acc, pin)
        if not user:
            return "User not found"

        if amount <= 0 or amount > self.AMOUNT_LIMIT:
            return f"Invalid amount. Maximum allowed is {self.AMOUNT_LIMIT}"

        user["Balance"] += amount
        
        # Add transaction record
        if "Transactions" not in user:
            user["Transactions"] = []
        
        user["Transactions"].append({
            "Type": "Deposit",
            "Amount": amount,
            "Balance": user["Balance"],
            "Timestamp": datetime.now().isoformat(),
            "Description": f"Deposited {amount}"
        })
        
        Bank.save()
        return user["Balance"]

    def withdraw(self, acc, pin, amount):
        user = self.find_user(acc, pin)
        if not user:
            return "User not found"

        if amount > user["Balance"]:
            return "Insufficient balance"

        user["Balance"] -= amount
        
        # Add transaction record
        if "Transactions" not in user:
            user["Transactions"] = []
        
        user["Transactions"].append({
            "Type": "Withdrawal",
            "Amount": amount,
            "Balance": user["Balance"],
            "Timestamp": datetime.now().isoformat(),
            "Description": f"Withdrew {amount}"
        })
        
        Bank.save()
        return user["Balance"]

    def delete(self, acc, pin):
        user = self.find_user(acc, pin)
        if not user:
            return "User not found"

        Bank.data.remove(user)
        Bank.save()
        return "Deleted"

    def get_transactions(self, acc, pin):
        """Retrieve transaction history for an account"""
        user = self.find_user(acc, pin)
        if not user:
            return None
        
        if "Transactions" not in user:
            user["Transactions"] = []
        
        return user["Transactions"]


# Load data when module is imported
Bank.load_data()