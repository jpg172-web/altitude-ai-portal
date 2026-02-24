import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import pdfplumber
from fuzzywuzzy import process

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(page_title="Cruise Advisory Solutions", layout="wide", initial_sidebar_state="expanded")

# --- 2. CUSTOM CSS FOR SAAS LOOK ---
st.markdown("""
    <style>
    .stApp { background-color: #F4F7F6; }
    div[data-testid="metric-container"] {
        background-color: white;
        border-radius: 12px;
        padding: 15px 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        border: 1px solid #E5E7EB;
    }
    section[data-testid="stSidebar"] {
        background-color: #1E5B94;
        color: white;
    }
    .stButton>button { width: 100%; border-radius: 5px; background-color: #2A75D3; color: white; }
    </style>
""", unsafe_allow_html=True)

# --- 3. HELPER FUNCTIONS ---
def extract_pdf_table(pdf_file):
    try:
        with pdfplumber.open(pdf_file) as pdf:
            page = pdf.pages[0]
            table = page.extract_table()
            if table:
                df = pd.DataFrame(table[1:], columns=table[0])
                df.columns = [str(c).strip() for c in df.columns if c]
                return df
    except Exception as e:
        st.error(f"Error reading PDF: {e}")
    return None

def find_best_match(name, choices):
    match, score = process.extractOne(name, choices)
    return match if score > 80 else None

# --- 4. SIDEBAR NAVIGATION ---
with st.sidebar:
    st.title("✈️ Cruise Advisory")
    page = st.radio("Navigation", ["Overview", "Spend Analysis", "Invoices", "Admin"])
    st.divider()
    st.write("👤 **John Doe**")
    st.caption("Admin")
    if st.button("Logout"):
        st.info("Session Ended.")

# --- 5. PAGE ROUTING ---

# PAGE: OVERVIEW (Your Mockup Design)
if page == "Overview":
    st.title("Welcome back, John Doe")
    st.write("---")
    
    # KPI Cards
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Total Spend", "$845,230", "+12%")
    k2.metric("Auto Approved", "81.5%", "134/165")
    k3.metric("Open Exceptions", "6", "Action Required", delta_color="inverse")
    k4.metric("Variance Identified", "$25,870", "Saved")

    # Charts
    c1, c2 = st.columns([2, 1])
    with c1:
        st.subheader("Monthly Spend & Variance")
        df_trend = pd.DataFrame({"Month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"], "Expected": [1500, 1800, 2100, 1900, 2400, 2600], "Actual": [1600, 1850, 2300, 1950, 2600, 2900]})
        fig = go.Figure()
        fig.add_trace(go.Bar(x=df_trend['Month'], y=df_trend['Expected'], name='Expected', marker_color='#A3C1DA'))
        fig.add_trace(go.Bar(x=df_trend['Month'], y=df_trend['Actual'], name='Actual', marker_color='#2A75D3'))
        st.plotly_chart(fig, use_container_width=True)
    
    with c2:
        st.subheader("Spend by Airport")
        df_airport = pd.DataFrame({"Airport": ["MIA", "LAX", "JFK", "ATL", "Others"], "Spend": [250410, 137908, 143163, 7003617, 395232]})
        fig2 = px.pie(df_airport, values='Spend', names='Airport', hole=0.5)
        st.plotly_chart(fig2, use_container_width=True)

# PAGE: INVOICES (Functional Audit Engine)
elif page == "Invoices":
    st.title("📂 Altitude-Ai Audit Workspace")
    col_in, col_out = st.columns([1, 2])
    
    with col_in:
        st.subheader("Data Upload")
        contract_file = st.file_uploader("Upload Master Contract (Excel)", type="xlsx")
        invoice_file = st.file_uploader("Upload PDF Invoice", type="pdf")
        
        if contract_file and invoice_file:
            df_contract = pd.read_excel(contract_file)
            df_invoice = extract_pdf_table(invoice_file)
            
            if df_invoice is not None:
                svc_col = st.selectbox("Service Column", options=df_invoice.columns)
                rate_col = st.selectbox("Rate Column", options=df_invoice.columns)
                
                if st.button("Run Reconciliation"):
                    # Process & Clean
                    df_invoice = df_invoice.rename(columns={svc_col: "Service", rate_col: "Invoice_Rate"})
                    df_invoice['Invoice_Rate'] = pd.to_numeric(df_invoice['Invoice_Rate'].replace(r'[\$,]', '', regex=True), errors='coerce')
                    
                    # Matching Logic
                    df_invoice['Match'] = df_invoice['Service'].apply(lambda x: find_best_match(str(x), df_contract['Service'].tolist()))
                    results = pd.merge(df_invoice, df_contract, left_on="Match", right_on="Service", how="left", suffixes=('_Inv', '_Con'))
                    results['Variance'] = results['Invoice_Rate'] - results['Contract_Rate']
                    
                    st.session_state['audit_results'] = results
                    st.success("Audit Complete!")

    with col_out:
        st.subheader("Audit Results")
        if 'audit_results' in st.session_state:
            res = st.session_state['audit_results']
            overcharges = res[res['Variance'] > 0]
            if not overcharges.empty:
                st.error(f"Alert: {len(overcharges)} line items exceed contract rates!")
                st.dataframe(overcharges[['Service_Inv', 'Invoice_Rate', 'Contract_Rate', 'Variance']], use_container_width=True)
            else:
                st.success("No variances detected. All charges align with contract.")
        else:
            st.info("Upload documents and click 'Run Reconciliation' to see the audit trail.")