import streamlit as st
from bank import Bank
import pandas as pd

bank = Bank()


def start_index_at_one(df):
    display_df = df.copy()
    display_df.index = display_df.index + 1
    return display_df

st.set_page_config(page_title="Banking System", page_icon="🏦", layout="wide")
st.title("🏦 Simple Banking System")

menu = st.sidebar.selectbox("Choose Option", [
    "Home",
    "View Customers",
    "Create Account",
    "Deposit",
    "Withdraw",
    "Check Details",
    "Transaction History",
    "Delete Account"
])

# ---------------- HOME DASHBOARD ----------------
if menu == "Home":
    st.subheader("📊 Banking Dashboard")
    
    col1, col2 = st.columns(2)
    
    total_accounts = len(bank.data)
    total_balance = sum((acc.get("Balance") or 0) for acc in bank.data)
    
    with col1:
        st.metric("Total Accounts", total_accounts)
    with col2:
        st.metric("Total Balance", f"₹{total_balance:,.2f}")
    
    st.divider()
    
    if total_accounts > 0:
        st.subheader("Top 5 Accounts by Balance")
        top_accounts = sorted(bank.data, key=lambda x: x.get("Balance", 0), reverse=True)[:5]
        
        account_df = pd.DataFrame([
            {
                "Name": acc["name"],
                "Account No": acc["AccountNo"],
                "Balance": f"₹{acc.get('Balance', 0):,.2f}",
                "Email": acc["E-mail"]
            }
            for acc in top_accounts
        ])
        st.dataframe(start_index_at_one(account_df), use_container_width=True)
    else:
        st.info("No accounts yet. Create your first account!")

# ---------------- VIEW CUSTOMERS ----------------
elif menu == "View Customers":
    st.subheader("View Customers")

    if bank.data:
        customer_df = pd.DataFrame([
            {
                "Name": customer.get("name", ""),
                "Account No": customer.get("AccountNo", ""),
                "Email": customer.get("E-mail", "")
            }
            for customer in bank.data
        ])
        st.dataframe(start_index_at_one(customer_df), use_container_width=True)
    else:
        st.info("No customer data available yet.")

# ---------------- CREATE ACCOUNT ----------------
elif menu == "Create Account":
    st.subheader("Create Account")

    name = st.text_input("Name", key="create_name")
    age = st.number_input("Age", min_value=18, key="create_age")
    email = st.text_input("Email", key="create_email")
    pin = st.text_input("PIN", type="password", key="create_pin")

    if st.button("Create", key="create_btn"):
        try:
            result = bank.create_account(name, age, email, int(pin))
            if isinstance(result, dict):
                st.success("Account created successfully!")
                st.json(result)
            else:
                st.error(result)
        except ValueError:
            st.error("Invalid PIN. PIN must be 6 digits.")

# ---------------- DEPOSIT ----------------
elif menu == "Deposit":
    st.subheader("Deposit Money")
    st.caption(f"Maximum deposit amount: ₹{Bank.AMOUNT_LIMIT:,.0f}")

    acc = st.text_input("Account Number", key="dep_acc")
    pin = st.text_input("PIN", type="password", key="dep_pin")
    amount = st.number_input("Amount", key="dep_amount", min_value=0.0, max_value=float(Bank.AMOUNT_LIMIT))

    if st.button("Deposit", key="dep_btn"):
        try:
            result = bank.deposit(acc, int(pin), amount)
            if isinstance(result, str):
                st.error(result)
            else:
                st.success(f"Deposit successful! New balance: {result}")
        except ValueError:
            st.error("Invalid PIN. PIN must be 6 digits.")

# ---------------- WITHDRAW ----------------
elif menu == "Withdraw":
    st.subheader("Withdraw Money")

    acc = st.text_input("Account Number", key="wth_acc")
    pin = st.text_input("PIN", type="password", key="wth_pin")
    amount = st.number_input("Amount", key="wth_amount", min_value=0.0)

    if st.button("Withdraw", key="wth_btn"):
        try:
            result = bank.withdraw(acc, int(pin), amount)
            if isinstance(result, str):
                st.error(result)
            else:
                st.success(f"Withdrawal successful! New balance: {result}")
        except ValueError:
            st.error("Invalid PIN. PIN must be 6 digits.")

# ---------------- CHECK DETAILS ----------------
elif menu == "Check Details":
    st.subheader("Account Details")

    acc = st.text_input("Account Number", key="chk_acc")
    pin = st.text_input("PIN", type="password", key="chk_pin")

    if st.button("Check", key="chk_btn"):
        try:
            user = bank.find_user(acc, int(pin))
            if user:
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(f"**Name:** {user['name']}")
                    st.markdown(f"**Age:** {user['age']}")
                    st.markdown(f"**Email:** {user['E-mail']}")
                
                with col2:
                    st.metric("Account Balance", f"₹{user.get('Balance', 0):,.2f}")
                    st.markdown(f"**Account No:** {user['AccountNo']}")
                
                st.divider()
                
                # Display recent transactions
                transactions = user.get("Transactions", [])
                if transactions:
                    st.subheader("📋 Recent Transactions")
                    recent_txn = transactions[-5:]  # Show last 5
                    
                    txn_df = pd.DataFrame([
                        {
                            "Date": pd.to_datetime(t["Timestamp"]).strftime("%Y-%m-%d %H:%M"),
                            "Type": t["Type"],
                            "Amount": f"₹{t['Amount']:,.2f}",
                            "Balance": f"₹{t['Balance']:,.2f}",
                            "Description": t.get("Description", "")
                        }
                        for t in recent_txn
                    ])
                    st.dataframe(start_index_at_one(txn_df), use_container_width=True)
                else:
                    st.info("No transactions yet")
            else:
                st.error("User not found")
        except ValueError:
            st.error("Invalid PIN. PIN must be 4 digits.")

# ---------------- TRANSACTION HISTORY ----------------
elif menu == "Transaction History":
    st.subheader("📊 Transaction History")

    acc = st.text_input("Account Number", key="txn_acc")
    pin = st.text_input("PIN", type="password", key="txn_pin")

    if st.button("View History", key="txn_btn"):
        try:
            transactions = bank.get_transactions(acc, int(pin))
            if transactions is not None:
                if transactions:
                    st.success(f"Found {len(transactions)} transactions")
                    
                    txn_df = pd.DataFrame([
                        {
                            "Date": pd.to_datetime(t["Timestamp"]).strftime("%Y-%m-%d %H:%M:%S"),
                            "Type": t["Type"],
                            "Amount": f"₹{t['Amount']:,.2f}",
                            "Balance": f"₹{t['Balance']:,.2f}",
                            "Description": t.get("Description", "")
                        }
                        for t in transactions
                    ])
                    st.dataframe(start_index_at_one(txn_df), use_container_width=True)
                    
                    # Summary stats
                    col1, col2, col3 = st.columns(3)
                    deposits = sum(t["Amount"] for t in transactions if t["Type"] == "Deposit")
                    withdrawals = sum(t["Amount"] for t in transactions if t["Type"] == "Withdrawal")
                    
                    with col1:
                        st.metric("Total Deposits", f"₹{deposits:,.2f}")
                    with col2:
                        st.metric("Total Withdrawals", f"₹{withdrawals:,.2f}")
                    with col3:
                        st.metric("Net Change", f"₹{deposits - withdrawals:,.2f}")
                else:
                    st.info("No transactions yet")
            else:
                st.error("User not found")
        except ValueError:
            st.error("Invalid PIN. PIN must be 6 digits.")

# ---------------- DELETE ----------------
elif menu == "Delete Account":
    st.subheader("Delete Account")

    acc = st.text_input("Account Number", key="del_acc")
    pin = st.text_input("PIN", type="password", key="del_pin")

    if st.button("Delete", key="del_btn"):
        try:
            result = bank.delete(acc, int(pin))
            if result == "Deleted":
                st.success("Account deleted successfully!")
            else:
                st.error(result)
        except ValueError:
            st.error("Invalid PIN. PIN must be 6 digits.")