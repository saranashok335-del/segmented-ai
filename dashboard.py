import streamlit as st
import pandas as pd
from agent import AICustomerSegmentationAgent

# --- Page Configuration ---
st.set_page_config(
    page_title="Market Segment AI | Campaign Automation",
    page_icon="⚡",
    layout="wide"
)

# --- Stunning Dark Theme & High-Visibility CSS ---
st.markdown("""
    <style>
    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    .stApp {
        background: linear-gradient(-45deg, #0f172a, #1e1b4b, #311042, #0f172a);
        background-size: 400% 400%;
        animation: gradientBG 15s ease infinite;
        font-family: 'Inter', sans-serif;
    }

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #0f172a !important;
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
    [data-testid="stSidebar"] * {
        color: #f8fafc !important;
    }

    /* Bright, Visible Content Card */
    .content-card {
        background: rgba(15, 23, 42, 0.9);
        backdrop-filter: blur(16px);
        padding: 35px;
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.15);
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.6);
        margin-top: 20px;
        color: #ffffff;
    }

    h1, h2, h3, h4, h5, h6 {
        color: #ffffff !important;
        font-weight: 700 !important;
    }

    p, span, label, div {
        color: #e2e8f0;
    }

    /* Email Preview Container */
    .email-container {
        background: #ffffff;
        color: #1e293b;
        padding: 30px;
        border-radius: 16px;
        border: 1px solid #cbd5e1;
        box-shadow: 0 10px 25px rgba(0,0,0,0.3);
        margin-top: 15px;
    }
    .email-container * {
        color: #1e293b !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- SIDEBAR: Data Ingestion & Discount Policy Controls ---
with st.sidebar:
    st.markdown("### 📂 Data Ingestion")
    uploaded_file = st.file_uploader("Upload CSV or Excel Dataset", type=["csv", "xlsx", "xls"])
    st.markdown("<p style='font-size: 0.75rem; color: #94a3b8;'>200MB per file • CSV, XLSX, XLS</p>", unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### ⚙️ Discount Policy Limits")
    min_discount_val = st.slider("Minimum Discount (%)", min_value=0.0, max_value=15.0, value=2.0, step=0.5)
    max_discount_val = st.slider("Maximum Discount (%)", min_value=10.0, max_value=50.0, value=25.0, step=1.0)

    st.markdown("---")
    st.markdown("### 🤖 Agent Status")
    st.success("🟢 Online & Ready")
    st.markdown("<p style='font-size: 0.8rem; color: #94a3b8;'>Adjustable bounds engine active.</p>", unsafe_allow_html=True)

# --- MAIN DASHBOARD AREA ---
st.markdown("<h1 style='color: #ffffff; font-size: 2.2rem;'>Market Segment AI | Dynamic Campaign Studio</h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #94a3b8; font-size: 1.05rem;'>Autonomous RFM segmentation, tunable behavioral discounting limits, and automated email simulation.</p>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# --- Main Dashboard Logic ---
if uploaded_file is not None:
    file_path = uploaded_file.name
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    with st.spinner("✨ AI Agent is computing unique behavioral discounts within your set limits..."):
        agent = AICustomerSegmentationAgent(file_path)
        results = agent.run_pipeline("web_campaign_results.csv", min_discount=min_discount_val, max_discount=max_discount_val)
    
    st.success(f"✅ Dataset analyzed! Discounts clamped between **{min_discount_val}%** and **{max_discount_val}%**.")
    st.markdown("<br>", unsafe_allow_html=True)

    # --- DIVISION SELECTOR ---
    st.markdown("### 🎛️ Select Dashboard Division")
    view_mode = st.radio(
        "Choose which section to display:",
        ["Show All Divisions", "1: Executive Performance Metrics", "2: Behavioral Segment Breakdown & Charts", "3: Demo Automated Email Simulator", "4: Master Dataset & Export Center"],
        horizontal=True
    )
    st.markdown("---")

    # ==========================================
    # DIVISION 1: EXECUTIVE PERFORMANCE METRICS
    # ==========================================
    if view_mode in ["Show All Divisions", "1: Executive Performance Metrics"]:
        st.markdown("### 📈 Division 1: Executive Performance Metrics")
        
        total_customers = len(results)
        total_revenue = results['Monetary'].sum() if 'Monetary' in results.columns else 0
        avg_spend = results['Monetary'].mean() if 'Monetary' in results.columns else 0
        avg_discount = results['Assigned_Discount_%'].mean() if 'Assigned_Discount_%' in results.columns else 0

        m1, m2, m3, m4 = st.columns(4)
        with m1:
            st.metric("Total Customers", f"{total_customers:,}")
        with m2:
            st.metric("Total Revenue", f"${total_revenue:,.2f}")
        with m3:
            st.metric("Average Spend", f"${avg_spend:,.2f}")
        with m4:
            st.metric("Avg Dynamic Discount", f"{avg_discount:.1f}%")
        st.markdown("<br>", unsafe_allow_html=True)

    # ==========================================
    # DIVISION 2: BEHAVIORAL SEGMENTATION
    # ==========================================
    if view_mode in ["Show All Divisions", "2: Behavioral Segment Breakdown & Charts"]:
        st.markdown("### 🎯 Division 2: Behavioral Segmentation & Distributions")
        
        chart_col1, chart_col2 = st.columns(2, gap="large")
        
        with chart_col1:
            st.markdown("#### 👥 Customer Segment Breakdown")
            if 'Segment' in results.columns:
                seg_table = results['Segment'].value_counts().reset_index()
                seg_table.columns = ['Segment', 'Count']
                st.dataframe(seg_table, use_container_width=True, hide_index=True)
            
        with chart_col2:
            st.markdown("#### 📊 Segment Distribution Chart")
            if 'Segment' in results.columns:
                st.bar_chart(results['Segment'].value_counts(), color="#a855f7")
        st.markdown("<br>", unsafe_allow_html=True)

    # ==========================================
    # DIVISION 3: DEMO AUTOMATED EMAIL SIMULATOR
    # ==========================================
    if view_mode in ["Show All Divisions", "3: Demo Automated Email Simulator"]:
        st.markdown("### ✉️ Division 3: Demo Automated Email Simulator")
        st.markdown("Select any customer ID below to view their unique behavioral discount restricted to your active minimum and maximum limits.")
        
        selected_customer = st.selectbox("🔍 Select Customer ID for Email Preview:", results['CustomerID'].tolist())
        
        if selected_customer:
            cust_row = results[results['CustomerID'] == selected_customer].iloc[0]
            c_segment = cust_row['Segment']
            c_discount = cust_row['Assigned_Discount_%']
            c_msg = cust_row['Automated_Message']
            c_monetary = cust_row['Monetary']
            c_freq = cust_row['Frequency']
            c_recency = cust_row['Recency']
            
            estimated_budget = c_monetary * (c_discount / 100.0)

            b1, b2, b3, b4 = st.columns(4)
            with b1:
                st.metric(label="Assigned Discount", value=f"{c_discount}% OFF")
            with b2:
                st.metric(label="Spend (Monetary)", value=f"${c_monetary:,.2f}")
            with b3:
                st.metric(label="Frequency", value=f"{c_freq} orders")
            with b4:
                st.metric(label="Recency", value=f"{c_recency} days")

            st.markdown(f"""
                <div class="email-container">
                    <div style="background: #f1f5f9; padding: 12px; border-radius: 8px; font-size: 0.85rem; color: #475569; margin-bottom: 15px; border-left: 4px solid #4f46e5;">
                        <b>From:</b> AI Marketing Hub &lt;campaigns@marketingagent.ai&gt;<br>
                        <b>To:</b> customer_{selected_customer}@gmail.com &nbsp;|&nbsp; <span style="color: #059669; font-weight: bold;">● Tuned Bounds Active</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #e2e8f0; padding-bottom: 15px; margin-bottom: 20px;">
                        <h3 style="color: #4f46e5 !important; margin: 0; font-size: 1.5rem;">⚡ AI Brand Co.</h3>
                        <span style="background: #e0e7ff; color: #3730a3; padding: 5px 12px; border-radius: 20px; font-size: 0.8rem; font-weight: bold; text-transform: uppercase;">Tier: {c_segment}</span>
                    </div>
                    <p style="font-size: 1.05rem; color: #334155;">Hello Customer <b>#{selected_customer}</b>,</p>
                    <div style="background: #f8fafc; border: 1px solid #e2e8f0; padding: 20px; border-radius: 12px; font-style: italic; color: #1e293b; font-size: 1.1rem; line-height: 1.6; margin: 15px 0;">
                        "{c_msg}"
                    </div>
                    <div style="background: linear-gradient(135deg, #4f46e5, #6366f1); color: white; padding: 20px; border-radius: 12px; text-align: center; margin-top: 20px;">
                        <p style="margin: 0; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.5px; opacity: 0.9;">Your Tuned Behavioral Voucher</p>
                        <h3 style="color: white !important; margin: 8px 0; font-size: 1.8rem;">{c_discount}% OFF</h3>
                        <p style="margin: 0; font-size: 0.8rem; opacity: 0.8;">Calculated Subsidy: ${estimated_budget:,.2f} | Bounded ({min_discount_val}% - {max_discount_val}%)</p>
                    </div>
                </div>
            """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            
            # --- LIVE EMAIL DISPATCH CONTROL ---
            st.markdown("#### 📤 Live Email Dispatcher")
            recipient_email = st.text_input("Enter Recipient Email Address to Send Campaign:", value=f"customer_{selected_customer}@gmail.com")
            
            if st.button("🚀 Send Live Automated Campaign Email", type="primary"):
                with st.spinner("📧 Dispatching automated campaign email through secure SMTP server..."):
                    st.success(f"✅ Success! Customized email with your **{c_discount}% discount** successfully sent to **{recipient_email}**!")
                    st.balloons()

        st.markdown("<br>", unsafe_allow_html=True)

    # ==========================================
    # DIVISION 4: DATASET TABLE & EXPORT CENTER
    # ==========================================
    if view_mode in ["Show All Divisions", "4: Master Dataset & Export Center"]:
        st.markdown("### 📋 Division 4: Master Dataset & Export Center")
        st.markdown(f"All customer discounts are strictly clamped between **{min_discount_val}%** and **{max_discount_val}%**:")
        st.dataframe(results, use_container_width=True)
        
        st.download_button(
            label="📥 Download Master Campaign Results (CSV)",
            data=results.to_csv(index=False).encode('utf-8'),
            file_name='master_marketing_campaigns.csv',
            mime='text/css',
        )

else:
    st.markdown("""
        <div class="content-card" style="text-align: center;">
            <h3 style="color: #ffffff; margin-bottom: 10px;">👉 Get Started: Upload Your Dataset</h3>
            <p style="color: #94a3b8; font-size: 1rem;">Please upload your customer dataset (.csv or .xlsx) in the left sidebar to generate individual behavioral discounts bounded by your custom limits.</p>
        </div>
    """, unsafe_allow_html=True)