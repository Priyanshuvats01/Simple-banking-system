# Simple Banking System

This project is a small banking application built with a Streamlit frontend and a Python backend. It lets users create accounts, deposit money, withdraw money, view account details, inspect transaction history, and delete accounts. Account data is stored locally in `data.json`.

## Features

- Create a bank account with name, age, email, and PIN
- Deposit money into an existing account
- Withdraw money from an existing account
- View customer list and account details
- See recent transactions and full transaction history
- Delete an account when needed
- Dashboard summary with total accounts, total balance, and top accounts

## Project Structure

- `app.py` - Streamlit web interface and user interactions
- `bank.py` - Core banking logic, validation, and JSON persistence
- `data.json` - Local storage file for account data
- `main.py` - Legacy console-based version kept for reference

## How It Works

The app UI in `app.py` creates a `Bank` object from `bank.py` and calls its methods for every action. The backend keeps all account information in memory and saves changes back to `data.json` after each operation.

Each account stores:

- name
- age
- email
- PIN
- account number
- balance
- creation timestamp
- transaction history

## Requirements

- Python 3.x
- Streamlit
- Pandas

Install dependencies with:

```bash
pip install streamlit pandas
```

## Run the Project

Start the Streamlit app with:

```bash
streamlit run app.py
```

When the app starts, it loads existing account data from `data.json`. If the file does not exist yet, it is created automatically.

## Notes

- The main application is `app.py`;
- Account PINs in the current backend are 6 digits.
- Deposit amounts are limited by `Bank.AMOUNT_LIMIT` in `bank.py`.

## Example Workflow

1. Open the app with Streamlit.
2. Create a new account.
3. Use the generated account number and PIN to deposit or withdraw money.
4. Check account details or transaction history from the sidebar menu.

