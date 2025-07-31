import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Set random seed for reproducible data
np.random.seed(42)

# Create fake expense data
def create_fake_expenses(num_expenses=30):
    names = ["John", "Sarah", "Mike", "Emma", "David", "Lisa", "Alex", "Maria", "Tom", "Anna"]
    categories = ["Food", "Transport", "Entertainment", "Shopping", "Bills"]
    payment_methods = ["Cash", "Card"]
    card_types = ["Chase", "Capital One", "Bilt", "Discover", "Debit"]
    
    expenses = []
    end_date = datetime.now()
    start_date = end_date - timedelta(days=90)
    
    for i in range(num_expenses):
        expense = {
            "name": random.choice(names),
            "amount": round(random.uniform(5, 200), 2),
            "date": start_date + timedelta(days=random.randint(0, 90)),
            "category": random.choice(categories),
            "payment_method": random.choice(payment_methods),
            "card_type": random.choice(card_types) if random.choice(payment_methods) == "Card" else None
        }
        expenses.append(expense)
    
    return pd.DataFrame(expenses)

# Create fake data
fake_df = create_fake_expenses(50)

# Leaderboard functions
def create_spending_leaderboard(df):
    """Create a leaderboard of top spenders"""
    st.subheader("🏆 Top Spenders")
    
    # Group by name and sum amounts
    spending_by_person = df.groupby('name')['amount'].agg(['sum', 'count']).reset_index()
    spending_by_person.columns = ['Name', 'Total Spent', 'Number of Expenses']
    spending_by_person = spending_by_person.sort_values('Total Spent', ascending=False)
    
    # Display leaderboard
    for i, (_, row) in enumerate(spending_by_person.head(10).iterrows(), 1):
        col1, col2, col3, col4 = st.columns([0.1, 0.4, 0.3, 0.2])
        
        with col1:
            if i == 1:
                st.write("��")
            elif i == 2:
                st.write("��")
            elif i == 3:
                st.write("��")
            else:
                st.write(f"#{i}")
        
        with col2:
            st.write(f"**{row['Name']}**")
        
        with col3:
            st.write(f"${row['Total Spent']:.2f}")
        
        with col4:
            st.write(f"({row['Number of Expenses']} expenses)")
    
    return spending_by_person

def create_frequency_leaderboard(df):
    """Create a leaderboard of most frequent spenders"""
    st.subheader("📊 Most Frequent Spenders")
    
    # Count expenses by name
    frequency_by_person = df['name'].value_counts().reset_index()
    frequency_by_person.columns = ['Name', 'Number of Expenses']
    
    # Add total spent for each person
    spending_by_person = df.groupby('name')['amount'].sum().reset_index()
    frequency_by_person = frequency_by_person.merge(spending_by_person, on='Name')
    frequency_by_person.columns = ['Name', 'Number of Expenses', 'Total Spent']
    
    # Display leaderboard
    for i, (_, row) in enumerate(frequency_by_person.head(10).iterrows(), 1):
        col1, col2, col3, col4 = st.columns([0.1, 0.4, 0.3, 0.2])
        
        with col1:
            if i == 1:
                st.write("⚡")
            elif i == 2:
                st.write("��")
            elif i == 3:
                st.write("��")
            else:
                st.write(f"#{i}")
        
        with col2:
            st.write(f"**{row['Name']}**")
        
        with col3:
            st.write(f"{row['Number of Expenses']} expenses")
        
        with col4:
            st.write(f"${row['Total Spent']:.2f}")
    
    return frequency_by_person

def create_payment_method_leaderboard(df):
    """Create a leaderboard of payment methods"""
    st.subheader("💳 Payment Method Leaderboard")
    
    # Group by payment method
    payment_stats = df.groupby('payment_method').agg({
        'amount': ['sum', 'count', 'mean']
    }).round(2)
    payment_stats.columns = ['Total Spent', 'Number of Transactions', 'Average Amount']
    payment_stats = payment_stats.sort_values('Total Spent', ascending=False)
    
    # Display leaderboard
    for i, (method, row) in enumerate(payment_stats.iterrows(), 1):
        col1, col2, col3, col4, col5 = st.columns([0.1, 0.3, 0.2, 0.2, 0.2])
        
        with col1:
            if i == 1:
                st.write("��")
            elif i == 2:
                st.write("��")
            else:
                st.write(f"#{i}")
        
        with col2:
            st.write(f"**{method}**")
        
        with col3:
            st.write(f"${row['Total Spent']:.2f}")
        
        with col4:
            st.write(f"{row['Number of Transactions']} transactions")
        
        with col5:
            st.write(f"${row['Average Amount']:.2f} avg")
    
    return payment_stats

def create_card_type_leaderboard(df):
    """Create a leaderboard of card types"""
    st.subheader("💳 Card Type Leaderboard")
    
    # Filter for card expenses only
    card_expenses = df[df['payment_method'] == 'Card']
    
    if not card_expenses.empty:
        # Group by card type
        card_stats = card_expenses.groupby('card_type').agg({
            'amount': ['sum', 'count', 'mean']
        }).round(2)
        card_stats.columns = ['Total Spent', 'Number of Transactions', 'Average Amount']
        card_stats = card_stats.sort_values('Total Spent', ascending=False)
        
        # Display leaderboard
        for i, (card_type, row) in enumerate(card_stats.iterrows(), 1):
            col1, col2, col3, col4, col5 = st.columns([0.1, 0.3, 0.2, 0.2, 0.2])
            
            with col1:
                if i == 1:
                    st.write("🏆")
                elif i == 2:
                    st.write("🥈")
                elif i == 3:
                    st.write("🥉")
                else:
                    st.write(f"#{i}")
            
            with col2:
                st.write(f"**{card_type}**")
            
            with col3:
                st.write(f"${row['Total Spent']:.2f}")
            
            with col4:
                st.write(f"{row['Number of Transactions']} transactions")
            
            with col5:
                st.write(f"${row['Average Amount']:.2f} avg")
        
        return card_stats
    else:
        st.info("No card expenses found!")
        return None

def create_category_leaderboard(df):
    """Create a leaderboard of spending categories"""
    st.subheader("📂 Category Leaderboard")
    
    # Group by category
    category_stats = df.groupby('category').agg({
        'amount': ['sum', 'count', 'mean']
    }).round(2)
    category_stats.columns = ['Total Spent', 'Number of Expenses', 'Average Amount']
    category_stats = category_stats.sort_values('Total Spent', ascending=False)
    
    # Display leaderboard
    for i, (category, row) in enumerate(category_stats.iterrows(), 1):
        col1, col2, col3, col4, col5 = st.columns([0.1, 0.3, 0.2, 0.2, 0.2])
        
        with col1:
            if i == 1:
                st.write("��")
            elif i == 2:
                st.write("��")
            elif i == 3:
                st.write("��")
            else:
                st.write(f"#{i}")
        
        with col2:
            st.write(f"**{category}**")
        
        with col3:
            st.write(f"${row['Total Spent']:.2f}")
        
        with col4:
            st.write(f"{row['Number of Expenses']} expenses")
        
        with col5:
            st.write(f"${row['Average Amount']:.2f} avg")
    
    return category_stats

# Main app
st.title("🏆 Expense Leaderboards")

# Show the fake data
st.subheader("📊 Sample Data")
st.write(f"Total expenses: {len(fake_df)}")
st.write(f"Date range: {fake_df['date'].min().strftime('%Y-%m-%d')} to {fake_df['date'].max().strftime('%Y-%m-%d')}")
st.write(f"Total amount: ${fake_df['amount'].sum():.2f}")

# Create tabs for different leaderboards
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "💰 Top Spenders", 
    "📊 Most Frequent", 
    "💳 Payment Methods", 
    "💳 Card Types", 
    "📂 Categories"
])

with tab1:
    create_spending_leaderboard(fake_df)

with tab2:
    create_frequency_leaderboard(fake_df)

with tab3:
    create_payment_method_leaderboard(fake_df)

with tab4:
    create_card_type_leaderboard(fake_df)

with tab5:
    create_category_leaderboard(fake_df)

# Summary statistics
st.subheader("📈 Leaderboard Summary")
col1, col2, col3, col4 = st.columns(4)

with col1:
    top_spender = fake_df.groupby('name')['amount'].sum().idxmax()
    top_amount = fake_df.groupby('name')['amount'].sum().max()
    st.metric("Top Spender", f"{top_spender}", f"${top_amount:.2f}")

with col2:
    most_frequent = fake_df['name'].value_counts().idxmax()
    freq_count = fake_df['name'].value_counts().max()
    st.metric("Most Frequent", f"{most_frequent}", f"{freq_count} expenses")

with col3:
    top_category = fake_df.groupby('category')['amount'].sum().idxmax()
    category_amount = fake_df.groupby('category')['amount'].sum().max()
    st.metric("Top Category", f"{top_category}", f"${category_amount:.2f}")

with col4:
    avg_expense = fake_df['amount'].mean()
    st.metric("Average Expense", f"${avg_expense:.2f}")

# Show raw data
st.subheader("�� Raw Data")
st.dataframe(fake_df, use_container_width=True)