"""
Mining Company Portal - Customized for Gold Fields
"""
import streamlit as st

# === SECURITY CHECK ===
# If not authenticated or not mining client, redirect to login
if not st.session_state.get('authenticated', False):
    st.error("🔒 Authentication required")
    st.stop()

if not st.session_state.get('show_mining_portal', False):
    st.error("⛔ Access Denied: Mining portal is exclusive to mining company clients")
    st.info("Please contact Guardian Ghana for mining client access")
    st.stop()

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np

st.set_page_config(
    page_title="Mining Operations Portal - Guardian Ghana",
    page_icon="⛏️",
    layout="wide"
)

# Professional mining portal styling
st.markdown("""
<style>
.mining-section {
    padding: 1.5rem;
    margin: 1rem 0;
    border-radius: 10px;
    border-left: 5px solid #d4af37;
    background-color: #f8f9fa;
}
.compliance-card {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 1.5rem;
    border-radius: 10px;
    margin: 1rem 0;
}
.risk-metric {
    font-size: 2.5rem;
    font-weight: bold;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# Header
col1, col2, col3 = st.columns([3, 1, 1])
with col1:
    st.title("⛏️ Mining Operations Portal")
    st.markdown("### Gold Fields Ghana - Environmental Monitoring Dashboard")
with col2:
    st.image("https://cdn-icons-png.flaticon.com/512/3067/3067256.png", width=80)
with col3:
    st.metric("🟢 Status", "Online", delta="All Systems Normal")

st.markdown("---")

# Mine Selection
st.sidebar.header("🏭 Mine Selection")
selected_mine = st.sidebar.selectbox(
    "Choose Mining Operation:",
    ["Tarkwa Gold Mine", "Damang Gold Mine", "Both Operations"],
    index=0
)

# Date Range
st.sidebar.header("📅 Date Range")
date_range = st.sidebar.date_input(
    "Select Period:",
    [datetime.now().date() - timedelta(days=30), datetime.now().date()]
)


# === SIMULATED MINING DATA ===
def generate_mining_operations_data(mine_name, days=30):
    """Generate realistic mining operation data"""

    dates = [datetime.now().date() - timedelta(days=i) for i in range(days)]
    data = []

    for date in dates:
        # Base values with daily variation
        base_turbidity = np.random.randint(40, 120)
        base_ph = np.random.uniform(6.2, 7.5)
        base_do = np.random.uniform(4.5, 7.5)

        # Operational events (5% chance)
        if np.random.random() > 0.95:
            base_turbidity *= np.random.uniform(1.5, 3.0)
            base_ph -= np.random.uniform(0.5, 1.2)

        # Weekend effect (lower activity)
        if date.weekday() >= 5:
            base_turbidity *= 0.7
            base_do *= 1.1

        # Compliance calculation
        compliance = "🟢 Compliant"
        if base_turbidity > 100 or base_ph < 6.0 or base_do < 5.0:
            compliance = "🔴 Non-Compliant"
        elif base_turbidity > 70 or base_ph < 6.5 or base_do < 6.0:
            compliance = "🟡 Warning"

        data.append({
            "Date": date,
            "Turbidity_NTU": base_turbidity,
            "pH": round(base_ph, 2),
            "Dissolved_Oxygen": round(base_do, 2),
            "Compliance_Status": compliance,
            "Mine": mine_name,
            "Daily_Throughput": np.random.randint(50000, 150000),
            "Water_Usage_m3": np.random.randint(5000, 15000),
            "Treatment_Cost_GH₵": np.random.randint(5000, 20000)
        })

    return pd.DataFrame(data)


# Generate data
tarkwa_data = generate_mining_operations_data("Tarkwa Mine", 30)
damang_data = generate_mining_operations_data("Damang Mine", 30)

if selected_mine == "Both Operations":
    mining_data = pd.concat([tarkwa_data, damang_data])
else:
    mining_data = tarkwa_data if "Tarkwa" in selected_mine else damang_data

# === DASHBOARD ===
st.markdown('<div class="mining-section">', unsafe_allow_html=True)
st.header(f"📊 {selected_mine} - Environmental Performance")

# Key Metrics
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    compliance_rate = (mining_data['Compliance_Status'] == "🟢 Compliant").mean() * 100
    st.metric("Compliance Rate", f"{compliance_rate:.1f}%",
              delta=f"{(compliance_rate - 95):+.1f}%" if compliance_rate else None)

with col2:
    avg_turbidity = mining_data['Turbidity_NTU'].mean()
    st.metric("Avg Turbidity", f"{avg_turbidity:.0f} NTU",
              delta="-5 NTU" if avg_turbidity < 75 else "+5 NTU")

with col3:
    avg_ph = mining_data['pH'].mean()
    st.metric("Avg pH", f"{avg_ph:.2f}",
              delta="Optimal" if 6.5 <= avg_ph <= 7.5 else "Review")

with col4:
    incidents = (mining_data['Compliance_Status'] == "🔴 Non-Compliant").sum()
    st.metric("Non-Compliance Incidents", incidents, delta="This Month")

with col5:
    water_usage = mining_data['Water_Usage_m3'].sum()
    st.metric("Total Water Usage", f"{water_usage:,} m³", delta="Monthly")

st.markdown('</div>', unsafe_allow_html=True)

# === COMPLIANCE ANALYTICS ===
st.markdown('<div class="mining-section">', unsafe_allow_html=True)
st.header("📈 Compliance Trend Analysis")

col1, col2 = st.columns(2)

with col1:
    # Compliance Trend Chart
    fig_compliance = px.line(mining_data, x='Date', y='Turbidity_NTU',
                             color='Mine' if selected_mine == "Both Operations" else None,
                             title='Turbidity Trend vs EPA Limit (100 NTU)',
                             labels={'Turbidity_NTU': 'Turbidity (NTU)', 'Date': 'Date'})

    # Add EPA limit line
    fig_compliance.add_hline(y=100, line_dash="dash", line_color="red",
                             annotation_text="EPA Limit", annotation_position="top right")

    st.plotly_chart(fig_compliance, use_container_width=True)

with col2:
    # pH Compliance Chart
    fig_ph = px.scatter(mining_data, x='Date', y='pH',
                        color='Compliance_Status',
                        title='pH Levels & Compliance Status',
                        labels={'pH': 'pH Level', 'Date': 'Date'},
                        color_discrete_map={
                            "🟢 Compliant": "green",
                            "🟡 Warning": "orange",
                            "🔴 Non-Compliant": "red"
                        })

    # Add pH range
    fig_ph.add_hrect(y0=6.0, y1=8.5, line_width=0, fillcolor="green", opacity=0.1,
                     annotation_text="EPA Range", annotation_position="top left")

    st.plotly_chart(fig_ph, use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

# === OPERATIONAL INTELLIGENCE ===
st.markdown('<div class="mining-section">', unsafe_allow_html=True)
st.header("🤖 AI Operational Intelligence")

col1, col2 = st.columns(2)

with col1:
    st.subheader("🚨 Risk Predictions")

    # Simulated AI predictions
    risk_predictions = [
        {"Parameter": "Turbidity", "Risk Level": "Low", "Confidence": "85%",
         "Prediction": "Stable for next 72 hours"},
        {"Parameter": "pH", "Risk Level": "Medium", "Confidence": "72%",
         "Prediction": "Possible acidification in 48-72h"},
        {"Parameter": "Dissolved Oxygen", "Risk Level": "Low", "Confidence": "90%",
         "Prediction": "Optimal levels maintained"},
        {"Parameter": "Upstream Impact", "Risk Level": "High", "Confidence": "68%",
         "Prediction": "Illegal mining activity detected upstream"}
    ]

    for prediction in risk_predictions:
        if prediction["Risk Level"] == "High":
            st.error(f"**{prediction['Parameter']}**: {prediction['Prediction']}")
        elif prediction["Risk Level"] == "Medium":
            st.warning(f"**{prediction['Parameter']}**: {prediction['Prediction']}")
        else:
            st.success(f"**{prediction['Parameter']}**: {prediction['Prediction']}")

with col2:
    st.subheader("💰 Cost-Benefit Analysis")

    # ROI Calculation
    current_cost = mining_data['Treatment_Cost_GH₵'].mean()
    predicted_savings = current_cost * 0.25  # 25% savings

    st.metric("Current Monthly Treatment Cost", f"GH₵{current_cost:,.0f}")
    st.metric("Predicted Monthly Savings", f"GH₵{predicted_savings:,.0f}",
              delta="25% reduction")
    st.metric("Projected Annual Savings", f"GH₵{predicted_savings * 12:,.0f}")

    st.info("""
    **ROI Timeline:**
    • **3 months:** Payback period
    • **12 months:** 300% ROI
    • **24 months:** Full system automation
    """)

st.markdown('</div>', unsafe_allow_html=True)

# === EPA REPORTING ===
st.markdown('<div class="mining-section">', unsafe_allow_html=True)
st.header("🏛️ EPA Compliance Reporting")

col1, col2 = st.columns(2)

with col1:
    st.subheader("📋 Automated Reports")

    report_types = [
        "Daily Operations Report",
        "Weekly Compliance Summary",
        "Monthly EPA Submission",
        "Quarterly Environmental Impact Assessment",
        "Annual Sustainability Report"
    ]

    for report in report_types:
        if st.button(f"Generate {report}", key=report):
            st.success(f"✅ {report} generated successfully!")
            st.download_button(
                label=f"📥 Download {report}",
                data=f"Sample {report} content for {selected_mine}",
                file_name=f"{report.replace(' ', '_')}_{datetime.now().date()}.txt",
                mime="text/plain"
            )

with col2:
    st.subheader("📊 Compliance Scorecard")

    # Calculate compliance metrics
    metrics = {
        "Turbidity Compliance": (mining_data['Turbidity_NTU'] <= 100).mean() * 100,
        "pH Compliance": ((mining_data['pH'] >= 6.0) & (mining_data['pH'] <= 8.5)).mean() * 100,
        "DO Compliance": (mining_data['Dissolved_Oxygen'] >= 5.0).mean() * 100,
        "Overall Compliance": compliance_rate
    }

    for metric, value in metrics.items():
        progress = value / 100
        st.write(f"**{metric}:** {value:.1f}%")
        st.progress(progress)
        st.caption("✅ EPA Standard Met" if value >= 95 else
                   "⚠️ Needs Improvement" if value >= 80 else
                   "❌ Below Standard")

st.markdown('</div>', unsafe_allow_html=True)

# === ALERT SYSTEM ===
st.markdown('<div class="mining-section">', unsafe_allow_html=True)
st.header("🚨 Alert & Notification System")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Alert Configuration")

    alert_channels = st.multiselect(
        "Notification Channels:",
        ["Email", "SMS", "Telegram", "Dashboard", "Siren"],
        default=["Email", "Telegram", "Dashboard"]
    )

    alert_thresholds = st.slider(
        "Turbidity Alert Threshold (NTU):",
        min_value=50, max_value=150, value=80, step=5
    )

    st.number_input("pH Alert Range - Min:", min_value=4.0, max_value=7.0, value=6.0, step=0.1)
    st.number_input("pH Alert Range - Max:", min_value=7.0, max_value=10.0, value=8.5, step=0.1)

with col2:
    st.subheader("Recent Alerts")

    # Simulated alerts
    recent_alerts = [
        {"time": "2 hours ago", "type": "⚠️ Warning", "message": "Turbidity approaching limit: 85 NTU"},
        {"time": "1 day ago", "type": "✅ Resolved", "message": "pH normalized to 7.2"},
        {"time": "3 days ago", "type": "🚨 Critical", "message": "Upstream illegal mining detected"},
        {"time": "1 week ago", "type": "🔔 Info", "message": "Monthly compliance report generated"}
    ]

    for alert in recent_alerts:
        if "Critical" in alert["type"]:
            st.error(f"{alert['type']}: {alert['message']} ({alert['time']})")
        elif "Warning" in alert["type"]:
            st.warning(f"{alert['type']}: {alert['message']} ({alert['time']})")
        else:
            st.info(f"{alert['type']}: {alert['message']} ({alert['time']})")

st.markdown('</div>', unsafe_allow_html=True)

# === FOOTER ===
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 2rem;">
    <h4>⛏️ Guardian Ghana Mining Portal</h4>
    <p>Designed specifically for Gold Fields Ghana environmental monitoring requirements</p>
    <p>📞 Contact: guardian.ghana.tech@gmail.com | 🌐 https://engchriss.github.io/guardianghana</p>
    <p><small>© 2025 Guardian Ghana. All mining data is simulated for demonstration purposes.</small></p>
</div>
""", unsafe_allow_html=True)

# Export all data button
if st.button("📥 Export All Mining Data (CSV)"):
    csv = mining_data.to_csv(index=False)
    st.download_button(
        label="Download CSV",
        data=csv,
        file_name=f"goldfields_mining_data_{datetime.now().date()}.csv",
        mime="text/csv"
    )