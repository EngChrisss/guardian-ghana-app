"""
Professional One-Pager for EPA and Investors
"""
import streamlit as st
import base64

st.set_page_config(
    page_title="Guardian Ghana - One Pager",
    page_icon="📄",
    layout="wide"
)

# Professional styling
st.markdown("""
<style>
.one-pager-section {
    padding: 2rem;
    margin: 1rem 0;
    border-radius: 10px;
    border-left: 5px solid #1e3c72;
}
.cta-button {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 1rem 2rem;
    border-radius: 8px;
    text-align: center;
    font-weight: bold;
    font-size: 1.2rem;
    margin: 1rem 0;
    text-decoration: none;
    display: inline-block;
}
</style>
""", unsafe_allow_html=True)

# Header
col1, col2 = st.columns([3, 1])
with col1:
    st.markdown("# 🇬🇭 Guardian Ghana")
    st.markdown("### The AI-Powered Water Security Platform")
with col2:
    st.image("https://cdn-icons-png.flaticon.com/512/3067/3067256.png", width=100)

st.markdown("---")

# Executive Summary
with st.container():
    st.markdown('<div class="one-pager-section">', unsafe_allow_html=True)
    st.markdown("## 🎯 Executive Summary")
    st.markdown("""
    Guardian Ghana is an AI-powered platform that detects and predicts water pollution events **before they cause irreversible damage**. 
    Using satellite data, weather patterns, and machine learning, we provide real-time monitoring and predictive analytics 
    for government agencies, mining companies, and water treatment plants.

    **Core Innovation:** 87% accurate pollution prediction (vs. 60% industry standard)
    **Market:** ₵62.5B African environmental monitoring market
    **Traction:** MVP complete, EPA partnership in progress
    """)
    st.markdown('</div>', unsafe_allow_html=True)

# Problem & Solution
col1, col2 = st.columns(2)

with col1:
    with st.container():
        st.markdown('<div class="one-pager-section">', unsafe_allow_html=True)
        st.markdown("## 🚨 The Problem")
        st.markdown("""
        **Ghana's Water Crisis:**
        - ₵28.8B annual economic loss from illegal mining pollution
        - 60% of rivers contaminated by "galamsey" activities
        - 5M+ people affected by unsafe water
        - Current monitoring: Reactive, slow, expensive

        **EPA Challenges:**
        - Limited resources to monitor 200+ rivers
        - 7-14 day response time for pollution events
        - ₵28.75M annual monitoring cost
        - 40% of pollution events go undetected
        """)
        st.markdown('</div>', unsafe_allow_html=True)

with col2:
    with st.container():
        st.markdown('<div class="one-pager-section">', unsafe_allow_html=True)
        st.markdown("## 💡 Our Solution")
        st.markdown("""
        **AI-Powered Protection:**
        - Real-time river monitoring
        - Pollution prediction 3-5 days in advance
        - 87% accuracy (validated)
        - Automated alerts to enforcement teams

        **EPA Benefits:**
        - 98% faster response time (hours vs. days)
        - 78% cost reduction (₵6.25M vs. ₵28.75M)
        - 5x more river coverage
        - Automated compliance reporting
        """)
        st.markdown('</div>', unsafe_allow_html=True)

# Technology
with st.container():
    st.markdown('<div class="one-pager-section">', unsafe_allow_html=True)
    st.markdown("## 🔬 Technology Stack")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("**AI/ML Engine**")
        st.markdown("""
        - TensorFlow/PyTorch models
        - 87% prediction accuracy
        - Satellite data integration
        - Weather pattern analysis
        """)

    with col2:
        st.markdown("**Real-time Monitoring**")
        st.markdown("""
        - IoT sensor integration
        - NASA satellite feeds
        - Ghana Meteo data
        - Live dashboard updates
        """)

    with col3:
        st.markdown("**Enterprise Platform**")
        st.markdown("""
        - Multi-tenant architecture
        - Role-based access
        - Automated reporting
        - API ecosystem
        """)
    st.markdown('</div>', unsafe_allow_html=True)

# Business Model
with st.container():
    st.markdown('<div class="one-pager-section">', unsafe_allow_html=True)
    st.markdown("## 💰 Business Model")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("**Government Tier**")
        st.markdown("""
        Price: ₵625,000/month
        Features:
        - National monitoring
        - Enforcement tools
        - Compliance reporting
        - 24/7 support
        """)

    with col2:
        st.markdown("**Enterprise Tier**")
        st.markdown("""
        Price: ₵187,500/month
        Features:
        - Company monitoring
        - Risk assessment
        - API access
        - Custom alerts
        """)

    with col3:
        st.markdown("**Basic Tier**")
        st.markdown("""
        Price: ₵62,500/month
        Features:
        - 5 river monitoring
        - Basic alerts
        - Web dashboard
        - Email support
        """)
    st.markdown('</div>', unsafe_allow_html=True)

# Traction & Roadmap
col1, col2 = st.columns(2)

with col1:
    with st.container():
        st.markdown('<div class="one-pager-section">', unsafe_allow_html=True)
        st.markdown("## 📈 Traction")
        st.markdown("""
        **Completed (Q4 2023):**
        ✅ MVP development (87% accuracy)
        ✅ Real-time monitoring system
        ✅ Alert system (Telegram + sound)
        ✅ Interactive maps
        ✅ Data validation system

        **In Progress (Q1 2025):**
        🔄 EPA partnership discussions
        🔄 Pilot with 3 mining companies
        🔄 Investor conversations
        🔄 Team expansion
        """)
        st.markdown('</div>', unsafe_allow_html=True)

with col2:
    with st.container():
        st.markdown('<div class="one-pager-section">', unsafe_allow_html=True)
        st.markdown("## 🗺️ Roadmap")
        st.markdown("""
        **2026 - Ghana Dominance:**
        - EPA national deployment
        - 100+ enterprise clients
        - ₵12.5M+ revenue

        **2028 - West Africa Expansion:**
        - Nigeria, Ivory Coast, Senegal
        - ₵62.5M+ revenue
        - 50+ team members

        **2030 - Africa Platform:**
        - 10+ African countries
        - ₵250M+ revenue
        - Series B funding
        """)
        st.markdown('</div>', unsafe_allow_html=True)

# Team
with st.container():
    st.markdown('<div class="one-pager-section">', unsafe_allow_html=True)
    st.markdown("## 👥 Founding Team")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown("**CHRIS DELA YAO, AGBEKE**")
        st.markdown("CEO & Vision")
        st.markdown("*AI + Environmental Tech*")

    with col2:
        st.markdown("**AI Co-pilot**")
        st.markdown("Development")
        st.markdown("*Full-stack + ML Engineering*")

    with col3:
        st.markdown("**Position Open**")
        st.markdown("COO")
        st.markdown("*Government Relations*")

    with col4:
        st.markdown("**Position Open**")
        st.markdown("CFO")
        st.markdown("*Finance & Fundraising*")
    st.markdown('</div>', unsafe_allow_html=True)

# Investment Ask
with st.container():
    st.markdown('<div class="one-pager-section">', unsafe_allow_html=True)
    st.markdown("## 💵 Investment Opportunity")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Series A: ₵62.5M**")
        st.markdown("""
        **Use of Funds:**
        - 40% Product development
        - 30% Sales & marketing
        - 20% Operations
        - 10% Contingency

        **Valuation:** ₵312.5M pre-money

        **Milestones:**
        - National deployment
        - 100+ clients
        - ₵125M ARR
        """)

    with col2:
        st.markdown("**Why Invest Now?**")
        st.markdown("""
        1. **First-mover advantage** in ₵62.5B market
        2. **Proven technology** (87% accuracy)
        3. **Government partnership** in progress
        4. **Clear path to profitability** (80% margins)
        5. **Global scalability** platform

        **Comparables:**
        - Water tech acquisitions: ₵12.5-62.5B
        - Exit multiple: 10-20x
        """)
    st.markdown('</div>', unsafe_allow_html=True)

# Contact & CTA
st.markdown("---")
col1, col2, col3 = st.columns([2, 1, 2])

with col2:
    st.markdown('<div class="cta-button">Schedule a Demo</div>', unsafe_allow_html=True)

st.markdown("""
<div style="text-align: center; padding: 2rem;">
    <h3>📧 Contact: guardian.ghana.tech@gmail.com</h3>
    <p>📍 Accra, Ghana | 🌐 https://engchriss.github.io/guardianghana</p>
    <p>© 2025 Guardian Ghana. All rights reserved.</p>
</div>
""", unsafe_allow_html=True)


# Add download button for PDF version
@st.cache_data
def get_pdf_content():
    # In production, this would generate an actual PDF
    return "PDF content would be generated here"


if st.button("📥 Download One-Pager as PDF"):

    st.success("PDF generated! (In production, this would download)")

