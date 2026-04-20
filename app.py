import streamlit as st
import pandas as pd
import numpy as np
from backend.rag_engine import get_interest_rate, get_max_multiplier

# Page Config
st.set_page_config(
    page_title="NexaBank AI - Aria Credit Officer",
    page_icon="🏦",
    layout="wide"
)

# Custom Styling (Glassmorphism inspired)
st.markdown("""
    <style>
    .main {
        background-color: #0f172a;
        color: #f8fafc;
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #38bdf8, #818cf8);
        color: white;
        font-weight: bold;
        border: none;
        border-radius: 10px;
        padding: 1rem;
        box-shadow: 0 4px 15px rgba(56, 189, 248, 0.4);
    }
    .stMetric {
        background: rgba(30, 41, 59, 0.7);
        padding: 1rem;
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    div[data-testid="stExpander"] {
        background: rgba(30, 41, 59, 0.5);
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# Application Header
st.title("🏦 Aria: Intelligent Credit Officer")
st.markdown("### Next-generation loan processing powered by RAG & Decision AI")

col1, col2 = st.columns([1, 1.5], gap="large")

with col1:
    st.header("📋 Application Data")
    with st.container(border=True):
        name = st.text_input("Full Name", "John Doe")
        age = st.number_input("Age", min_value=1, max_value=100, value=30)
        cibil = st.slider("CIBIL Score", 300, 900, 720)
        
        income_col1, income_col2 = st.columns(2)
        with income_col1:
            monthly_income = st.number_input("Monthly Income (₹)", value=50000)
        with income_col2:
            annual_income = st.number_input("Annual Income (₹)", value=600000)
            
        employment = st.selectbox("Employment Status", ["Salaried", "Self-Employed", "Freelancer"])
        existing_emis = st.number_input("Existing EMIs (₹)", value=10000)
        
        st.divider()
        
        loan_type = st.selectbox("Loan Type", ["Home", "Personal", "Business", "Vehicle", "Education"])
        loan_amount = st.number_input("Requested Loan Amount (₹)", value=500000)
        
        docs = st.multiselect("Documents Provided", ["Aadhaar", "PAN", "Bank Statement", "ITR"], default=["Aadhaar", "PAN", "Bank Statement"])

with col2:
    st.header("🤖 AI Decision Core")
    
    if st.button("🚀 One-Click AI Assessment"):
        with st.spinner("Aria is analyzing your application..."):
            # Internal Logic (Mirroring main.py)
            reasons = []
            status = "APPROVED"
            
            # 0. Age Limit
            if age < 18:
                reasons.append(f"Applicant age ({age}) is below the minimum legal requirement of 18 years.")
                status = "REJECTED"
            elif age > 70:
                reasons.append(f"Applicant age ({age}) exceeds the maximum threshold for loan maturity (70 years).")
                status = "REJECTED"
                
            # 1. Document Check
            required_docs = ["Aadhaar", "PAN", "Bank Statement"]
            if loan_type.lower() in ["home", "personal", "business"]:
                required_docs.append("ITR")
            
            missing_docs = [doc for doc in required_docs if doc not in docs]
            if missing_docs:
                reasons.append(f"Missing required documents for {loan_type} loan: {', '.join(missing_docs)}")
                status = "REJECTED"
                
            # 2. FOIR Check
            if monthly_income > 0:
                foir = (existing_emis / monthly_income) * 100
                if foir > 55:
                    reasons.append(f"FOIR ({foir:.2f}%) exceeds the 55% safety threshold.")
                    status = "REJECTED"
            
            # 3. CIBIL Check
            if cibil < 650:
                reasons.append(f"CIBIL score ({cibil}) is below the minimum required (650).")
                status = "REJECTED"
            elif 650 <= cibil <= 699:
                if status != "REJECTED":
                    status = "CONDITIONAL"
                    reasons.append(f"CIBIL score ({cibil}) is marginal. Additional collateral recommended.")
            
            # 4. Loan-to-Income
            max_mult = get_max_multiplier(loan_type)
            max_loan = annual_income * max_mult
            if loan_amount > max_loan:
                reasons.append(f"Requested amount ({loan_amount}) exceeds the allowed limit ({max_loan}) for this income level.")
                if status != "REJECTED":
                    status = "CONDITIONAL"

            # Display Results
            st.divider()
            
            if status == "APPROVED":
                st.success(f"### Assessment: {status}")
                st.balloons()
            elif status == "REJECTED":
                st.error(f"### Assessment: {status}")
            else:
                st.warning(f"### Assessment: {status}")
            
            st.subheader("📝 Decision Logic")
            for r in reasons if reasons else ["All primary checks passed. Parameters within acceptable range."]:
                st.write(f"- {r}")
                
            res_col1, res_col2 = st.columns(2)
            with res_col1:
                st.metric("Interest Rate", get_interest_rate(loan_type))
            with res_col2:
                st.metric("Max Eligible Limit", f"₹{max_loan}")
                
            if status == "APPROVED":
                with st.expander("✅ Next Steps for Disbursement"):
                    st.write("1. E-Sign Loan Agreement")
                    st.write("2. Setup e-Mandate")
                    st.write("3. Penny-Drop Verification")
                    st.write("4. Fund Credit (24hrs)")
            elif status != "REJECTED":
                with st.expander("💡 Suggested Alternatives"):
                    st.write(f"- Reduce loan amount to ₹{max_loan * 0.8}")
                    st.write("- Add a co-applicant with CIBIL > 750")
    else:
        st.info("Fill out the form on the left and click 'One-Click AI Assessment' to begin.")

st.sidebar.markdown("---")
st.sidebar.write("🏦 **NexaBank Systems Group**")
st.sidebar.write("🤖 **Agent ID:** Aria-904")
st.sidebar.markdown("---")
st.sidebar.image("https://img.icons8.com/isometric-line/100/38bdf8/bot.png")
