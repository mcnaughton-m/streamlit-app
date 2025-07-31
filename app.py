import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Initialize session state
if 'expenses' not in st.session_state:
    st.session_state.expenses = []

def load_expenses():
    if os.path.exists('expenses.csv'):
        df = pd.read_csv('expenses.csv')
        df['date'] = pd.to_datetime(df['date']).dt.date
        return df.to_dict('records')
    return []

def append_expense_to_csv(expense):
    """Append a single expense to the CSV file"""
    df_new = pd.DataFrame([expense])
    
    if os.path.exists('expenses.csv'):
        # Append without header (file already exists)
        df_new.to_csv('expenses.csv', mode='a', header=False, index=False)
    else:
        # Create new file with header
        df_new.to_csv('expenses.csv', index=False)

# Load existing data
if not st.session_state.expenses:
    st.session_state.expenses = load_expenses()

# Create tabs
tab1, tab2 = st.tabs([" Add Expenses", "📊 Charts & Analysis"])

# Tab 1: Add Expenses
with tab1:
    st.title("Add New Expense")
    
    with st.form(key="user_expense_form"):
        expense_name = st.text_input(label="Expense Name", placeholder="Enter Expense Name")
        expense_amount = st.number_input(label="Amount", min_value=0, step=1, value=0)
        expense_date = st.date_input(label="Date", value=datetime.now())
        expense_payment_method = st.radio(label="Payment Method", options=["Cash", "Card"])
        
        submitted = st.form_submit_button("Add Expense")

    
    # Process submission
    if submitted:
        expense = {
            "name": expense_name,
            "amount": expense_amount,
            "date": expense_date,
            "payment_method": expense_payment_method,
        }
        
        # Add to session state
        st.session_state.expenses.append(expense)
        
        # Append to CSV file
        append_expense_to_csv(expense)
        
        st.success("Expense added successfully!")

    st.image(os.path.join(os.getcwd(), "static", "monopoly_man.jpg"), width=1000)
# Tab 2: Charts
with tab2:
    st.title("Charts & Analysis")
    
    if st.session_state.expenses:
        df = pd.DataFrame(st.session_state.expenses)
        
        # Summary metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Expenses", len(df))
        with col2:
            st.metric("Total Spent", f"${df['amount'].sum():.2f}")
        with col3:
            st.metric("Average", f"${df['amount'].mean():.2f}")
        
        # Charts
        st.subheader(" Spending Over Time")
        st.line_chart(df.set_index('date')['amount'])
        
        st.subheader(" Payment Methods")
        payment_counts = df['payment_method'].value_counts()
        st.bar_chart(payment_counts)
        
        # Data table
        st.subheader("📋 All Expenses")
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No expenses yet. Add some in the first tab!")