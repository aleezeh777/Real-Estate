import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

sns.set_theme(style="darkgrid")

def calculate_roi(purchase_price, rental_income, expenses, appreciation_rate, years, down_payment):
    annual_cash_flow = (rental_income * 12) - expenses
    total_cash_flow = annual_cash_flow * years
    property_values = [purchase_price * ((1 + appreciation_rate / 100) ** i) for i in range(years + 1)]
    equities = [property_values[i] - (purchase_price - down_payment) for i in range(years + 1)]
    roi = ((total_cash_flow + equities[-1] - down_payment) / down_payment) * 100
    coc_roi = (annual_cash_flow / down_payment) * 100
    break_even_years = down_payment / annual_cash_flow if annual_cash_flow > 0 else float('inf')
    return roi, total_cash_flow, property_values, equities, coc_roi, break_even_years

def calculate_rent_vs_buy(rent, home_price, mortgage_rate, years, inflation_rate, down_payment):
    total_rent_paid = sum([rent * (1 + inflation_rate / 100) ** i for i in range(years)])
    
    if mortgage_rate > 0:
        loan_amount = home_price - down_payment
        monthly_rate = (mortgage_rate / 100) / 12
        num_payments = years * 12
        monthly_payment = (loan_amount * monthly_rate) / (1 - (1 + monthly_rate) ** -num_payments)
        total_home_cost = (monthly_payment * num_payments) + down_payment
    else:
        total_home_cost = home_price * ((1 + appreciation_rate / 100) ** years)
    
    break_even = None
    cumulative_rent = 0
    cumulative_buy = down_payment
    for t in range(1, years + 1):
        cumulative_rent += rent * (1 + inflation_rate / 100) ** (t - 1) * 12
        if mortgage_rate > 0:
            cumulative_buy += monthly_payment * 12
        if cumulative_buy <= cumulative_rent:
            break_even = t
            break
    
    return total_rent_paid, total_home_cost, break_even

st.set_page_config(page_title="Real Estate Investment Suite", layout="wide")
st.sidebar.title("🏠 Real Estate Investment Suite")

menu = st.sidebar.radio("Choose a Calculator", ["Overview", "ROI Calculator", "Rent vs. Buy"])

if menu == "Overview":
    st.title("📊 Real Estate Investment Overview")
    st.write("This tool helps you analyze real estate investments, compare renting vs. buying, and estimate potential returns.")
   
elif menu == "ROI Calculator":
    st.title("📈 Real Estate ROI Calculator")
    
    purchase_price = st.number_input("🏠 Purchase Price ($)", min_value=0, value=200000, step=1000)
    down_payment = st.number_input("💰 Down Payment ($)", min_value=0, value=40000, step=1000)
    rental_income = st.number_input("📅 Monthly Rental Income ($)", min_value=0, value=1500, step=100)
    expenses = st.number_input("💸 Annual Expenses ($)", min_value=0, value=5000, step=500)
    appreciation_rate = st.slider("📈 Annual Appreciation Rate (%)", min_value=0.0, max_value=10.0, value=3.0, step=0.1)
    years = st.slider("⏳ Investment Duration (Years)", min_value=1, max_value=30, value=10, step=1)
    
    if st.button("🚀 Calculate ROI"):
        roi, total_cash_flow, property_values, equities, coc_roi, break_even_years = calculate_roi(purchase_price, rental_income, expenses, appreciation_rate, years, down_payment)
        
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("📊 Investment Summary")
            st.markdown(f"**💵 Total Cash Flow:** ${total_cash_flow:,.2f}")
            st.markdown(f"**🏡 Property Value After {years} Years:** ${property_values[-1]:,.2f}")
            st.markdown(f"**📈 Equity Gained:** ${equities[-1]:,.2f}")
            st.markdown(f"**📊 ROI:** {roi:.2f}%")
            st.markdown(f"**💰 Cash-on-Cash ROI:** {coc_roi:.2f}%")
            st.markdown(f"**⏳ Break-even in:** {break_even_years:.2f} years")
        
        with col2:
            df = pd.DataFrame({"Year": list(range(years + 1)), "Property Value": property_values, "Equity": equities})
            
            fig, ax = plt.subplots(figsize=(8, 5))
            sns.lineplot(x=df["Year"], y=df["Property Value"], label="Property Value", marker="o", color="royalblue")
            sns.lineplot(x=df["Year"], y=df["Equity"], label="Equity", marker="^", color="green")
            ax.set_xlabel("Year")
            ax.set_ylabel("Amount ($)")
            ax.set_title("📈 Investment Growth Over Time")
            ax.legend()
            st.pyplot(fig)
    
elif menu == "Rent vs. Buy":
    st.title("🏡 Rent vs. Buy Calculator")
    
    rent = st.number_input("💸 Monthly Rent ($)", min_value=0, value=1500, step=100)
    home_price = st.number_input("🏠 Home Purchase Price ($)", min_value=0, value=200000, step=1000)
    mortgage_rate = st.slider("🏦 Mortgage Rate (%)", min_value=0.0, max_value=10.0, value=4.0, step=0.1)
    years = st.slider("⏳ Duration (Years)", min_value=1, max_value=30, value=10, step=1)
    inflation_rate = st.slider("📈 Rent Inflation Rate (%)", min_value=0.0, max_value=10.0, value=2.0, step=0.1)
    down_payment = st.number_input("💰 Down Payment ($)", min_value=0, value=40000, step=1000)  # Added down payment input

    if st.button("🔍 Compare"):
        total_rent_paid, total_home_cost, break_even = calculate_rent_vs_buy(rent, home_price, mortgage_rate, years, inflation_rate, down_payment)  # Passed down_payment here
        
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("📊 Cost Comparison")
            st.markdown(f"**🏠 Total Home Cost:** ${total_home_cost:,.2f}")
            st.markdown(f"**💸 Total Rent Paid:** ${total_rent_paid:,.2f}")
            st.markdown(f"**⚖️ Break-even Point:** {break_even if break_even else 'Never'} years")
        
        with col2:
            fig, ax = plt.subplots(figsize=(8, 5))
            labels = ["Total Rent Paid", "Total Home Cost"]
            sizes = [total_rent_paid, total_home_cost]
            colors = ["#ff9999", "#66b3ff"]
            ax.pie(sizes, labels=labels, autopct="%1.1f%%", colors=colors, startangle=90)
            ax.set_title("🏡 Rent vs. Buy Cost Distribution")
            st.pyplot(fig)
