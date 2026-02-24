import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import pdfplumber
from fuzzywuzzy import process

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(page_title="Cruise Advisory Solutions", page_icon="✈️", layout="wide", initial_sidebar_state="expanded")

# --- 2. CUSTOM CSS ---
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
    </style>
""", unsafe_allow_html=True)

# --- 3. SIDEBAR NAVIGATION ---
with st.sidebar:
    st.title("✈️ Cruise Advisory")
    page = st.radio("Navigation", ["Overview", "Spend Analysis", "Invoices", "Admin"])
    st.divider()
    # Updated to Kevin McGlinn
    st.write("👤 **Kevin McGlinn**")
    st.caption("Founder - CTO") 
    if st.button("Logout"):
        st.info("Session Ended.")

# --- 4. PAGE ROUTING ---

if page == "Overview":
    # Header update
    st.title("Welcome back, Kevin McGlinn")
    st.write("---")
    
    # KPI Cards (Matching your vision mockup)
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Total Spend", "$845,230", "+12%")
    k2.metric("Auto Approved", "81.5%", "134/165")
    k3.metric("Open Exceptions", "6", "Action Required", delta_color="inverse")
    k4.metric("Variance Identified", "$25,870", "Saved")

    # Charts Section
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

elif page == "Invoices":
    st.title("📂 Altitude-Ai Audit Workspace")
    st.info("Audit engine ready for Kevin McGlinn.")
    # (The rest of your functional audit logic remains here)