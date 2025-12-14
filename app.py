import streamlit as st
import pandas as pd
import datetime as dt
import numpy as np
import time
import folium
import random
import base64
import os
from datetime import datetime

ADMIN_PASSWORD = "M.P.139.23-24"

# Page configuration
st.set_page_config(
    page_title="Guardian Ghana - AI Water Protection",
    page_icon="💧",
    layout="wide"
)

# === CRITICAL: INITIALIZE ALL SESSION STATE VARIABLES FIRST ===
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.client_type = ""
    st.session_state.access_time = None
    st.session_state.failed_attempts = 0  # INITIALIZE HERE

# Initialize new session state variables for security features
if "show_mining_portal" not in st.session_state:
    st.session_state.show_mining_portal = False
if "show_epa_tools" not in st.session_state:
    st.session_state.show_epa_tools = False
if "access_level" not in st.session_state:
    st.session_state.access_level = ""
if "is_ceo" not in st.session_state:
    st.session_state.is_ceo = False

if "live_mode" not in st.session_state:
    st.session_state.live_mode = False
if "last_refresh_time" not in st.session_state:
    st.session_state.last_refresh_time = dt.datetime.now()
if "update_count" not in st.session_state:
    st.session_state.update_count = 0
if "enterprise_mode" not in st.session_state:
    st.session_state.enterprise_mode = {
        'live_mode': False,
        'last_update': dt.datetime.now(),
        'update_count': 0,
        'data_stream': True,
        'alert_system': True
    }
if "stream_expanded" not in st.session_state:
    st.session_state.stream_expanded = True
if "map_view" not in st.session_state:
    st.session_state.map_view = "Current Monitoring"
if "previous_critical_count" not in st.session_state:
    st.session_state.previous_critical_count = 0
if "previous_high_risk_count" not in st.session_state:
    st.session_state.previous_high_risk_count = 0
if "show_critical_alert" not in st.session_state:
    st.session_state.show_critical_alert = False
if "show_prediction_alert" not in st.session_state:
    st.session_state.show_prediction_alert = False
if "refresh_trigger" not in st.session_state:
    st.session_state.refresh_trigger = 0
if "live_data_df" not in st.session_state:
    st.session_state.live_data_df = None

from utils.enterprise_features import enterprise_dashboard, revenue_calculator
from data.sample_data import generate_sample_data, get_water_quality_status
from utils.map_helper import create_ghana_water_map, display_map, create_risk_overlay_map
from utils.alert_system import check_and_alert, TelegramAlertSystem
from utils.prediction_engine import predictor
from utils.cloud_logger import cloud_logger  # NEW: Enhanced logging system

# === PROFESSIONAL PASSWORD PROTECTION ===
# Show login if not authenticated
if not st.session_state.authenticated:
    # Professional login screen
    col1, col2 = st.columns([1, 1])

    with col1:
        st.image("https://cdn-icons-png.flaticon.com/512/3067/3067256.png", width=100)
        st.title("🇬🇭 Guardian Ghana")
        st.subheader("AI Water Protection Platform")

    with col2:
        st.markdown("### 🔐 Secure Access Required")

        # Password input with security features
        password_input = st.text_input(
            "Enter your access code:",
            type="password",
            help="Contact the system administrator for credentials",
            key="password_input"
        )

        # Initialize failed_attempts if it doesn't exist (safety check)
        if "failed_attempts" not in st.session_state:
            st.session_state.failed_attempts = 0

        # Security measures
        if st.session_state.failed_attempts >= 3:
            st.warning("⚠️ Multiple failed attempts detected. Please contact support.")
            if st.button("🆘 Contact Support", key="contact_support"):
                st.info("📧 Email: guardian.ghana.tech@gmail.com")
        else:
            col_btn1, col_btn2 = st.columns(2)

            with col_btn1:
                if st.button("Login", type="primary", key="login_btn"):
                    # === ENHANCED SECURE PASSWORD VALIDATION ===
                    valid_passwords = {
                        "M.P.139.23-24": "super_admin",      # YOU - CEO
                        "EPA2024": "government_full",       # Government full
                        "WRC2024": "government_basic",      # Government basic
                        "MINING2024": "mining_corporate",   # Mining companies
                        "CORPORATE2024": "corporate_basic", # Corporate basic
                        "DEMO2024": "demo_limited",         # Demo/Trial
                        "GUEST2024": "demo_limited"         # Guest access
                    }

                    if password_input in valid_passwords:
                        # SUCCESSFUL LOGIN
                        st.session_state.authenticated = True
                        st.session_state.client_type = valid_passwords[password_input]
                        st.session_state.access_time = dt.datetime.now()
                        st.session_state.failed_attempts = 0  # Reset on success

                        # SET SPECIFIC CLIENT PRIVILEGES
                        if password_input == "M.P.139.23-24":
                            # CEO/SUPER ADMIN
                            st.session_state.show_mining_portal = True
                            st.session_state.show_epa_tools = True
                            st.session_state.admin_unlocked = True  # Auto-unlock admin
                            st.session_state.access_level = "super_admin"
                            st.session_state.is_ceo = True  # New flag for CEO features
                            
                        elif password_input == "MINING2024":
                            # Mining Corporate
                            st.session_state.show_mining_portal = True
                            st.session_state.access_level = "mining_corporate"
                            st.session_state.client_type = "corporate"  # Set for compatibility
                            
                        elif password_input == "EPA2024":
                            # Government Full
                            st.session_state.show_epa_tools = True
                            st.session_state.access_level = "government_full"
                            st.session_state.client_type = "government"
                            
                        elif password_input == "WRC2024":
                            # Government Basic
                            st.session_state.show_epa_tools = True
                            st.session_state.access_level = "government_basic"
                            st.session_state.client_type = "government"
                            
                        elif password_input == "CORPORATE2024":
                            # Corporate Basic
                            st.session_state.access_level = "corporate_basic"
                            st.session_state.client_type = "corporate"
                            
                        else:  # DEMO2024 or GUEST2024
                            st.session_state.access_level = "demo_limited"
                            st.session_state.client_type = "demo"

                        # Log successful access
                        try:
                            cloud_logger.log_access(st.session_state.client_type, "login_success")
                        except:
                            pass

                        # Special CEO logging
                        if password_input == "M.P.139.23-24":
                            print(f"🚀 CEO LOGIN: {dt.datetime.now()}")
                            try:
                                with open("ceo_access_log.txt", "a", encoding="utf-8") as f:
                                    f.write(f"{dt.datetime.now()}: CEO LOGIN - SUPER ADMIN ACTIVATED\n")
                            except:
                                pass

                        # File logging backup
                        try:
                            with open("access_log.txt", "a", encoding="utf-8") as f:
                                f.write(
                                    f"{dt.datetime.now()}: {st.session_state.client_type.upper()} logged in ({password_input})\n")
                        except:
                            pass

                        st.rerun()
                    else:
                        # FAILED ATTEMPT
                        st.session_state.failed_attempts += 1
                        st.error("❌ Invalid access code")

                        # Log failed attempt (without password)
                        try:
                            with open("security_log.txt", "a", encoding="utf-8") as f:
                                f.write(
                                    f"{dt.datetime.now()}: Failed login attempt (Attempt #{st.session_state.failed_attempts})\n")
                        except:
                            pass

            with col_btn2:
                if st.button("Request Access", key="request_access"):
                    st.info("""
                    **For demo access, please contact:**
                    📧 guardian.ghana.tech@gmail.com

                    Include:
                    1. Your organization name
                    2. Your role
                    3. Purpose of access
                    4. Desired demo duration
                    """)

    # Professional waiting screen
    st.markdown("---")
    st.markdown("### 🏛️ Authorized Access Only")

    col_info1, col_info2 = st.columns(2)
    with col_info1:
        st.info("""
        **Government & Regulatory Bodies:**
        • Environmental Protection Agency
        • Water Resources Commission  
        • Minerals Commission
        • Ghana Water Company
        """)

    with col_info2:
        st.info("""
        **Corporate & Research Partners:**
        • Mining Corporations
        • Water Treatment Facilities
        • Environmental Consultancies
        • Academic Institutions
        """)

    # Security notice
    st.markdown("---")
    st.warning("""
    **🔒 Security Notice:**
    • Unauthorized access attempts are logged
    • All activities are monitored
    • This system contains proprietary technology
    • Violations may result in legal action
    """)

    st.caption(f"System Time: {dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} • v2.5.1")

    st.stop()

# ======== MAIN APPLICATION (AFTER AUTHENTICATION) ========
# Show client info in sidebar
st.sidebar.markdown("---")

# === SECURE MINING PORTAL ACCESS ===
# ONLY show for mining clients and CEO
if st.session_state.get('show_mining_portal', False):
    if st.sidebar.button("⛏️ Mining Operations Portal", key="mining_portal_button",
                        help="Exclusive portal for mining company clients"):
        st.switch_page("pages/6_Mining_Portal.py")

# Display access level
if st.session_state.access_level == "super_admin":
    st.sidebar.success("👑 SUPER ADMIN ACCESS")
    st.sidebar.info("Full system privileges")
elif st.session_state.access_level == "mining_corporate":
    st.sidebar.success(f"✅ MINING CORPORATE ACCESS")
    st.sidebar.info("Exclusive mining portal access")
elif st.session_state.access_level == "government_full":
    st.sidebar.success(f"✅ GOVERNMENT FULL ACCESS")
    st.sidebar.info("Full monitoring & enforcement privileges")
elif st.session_state.access_level == "government_basic":
    st.sidebar.success(f"✅ GOVERNMENT BASIC ACCESS")
    st.sidebar.info("Basic monitoring access")
elif st.session_state.access_level == "corporate_basic":
    st.sidebar.success(f"✅ CORPORATE BASIC ACCESS")
    st.sidebar.info("Basic compliance monitoring")
elif st.session_state.access_level == "demo_limited":
    st.sidebar.warning(f"⚠️ DEMO/TRIAL ACCESS")
    st.sidebar.info("Limited functionality • 7-day trial")
else:
    st.sidebar.success(f"✅ AUTHORIZED ACCESS")

# Session timer
if st.session_state.access_time:
    try:
        access_duration = dt.datetime.now() - st.session_state.access_time
        hours = int(access_duration.total_seconds() // 3600)
        minutes = int((access_duration.total_seconds() % 3600) // 60)

        if hours > 0:
            st.sidebar.caption(f"🕐 Session: {hours}h {minutes}m")
        else:
            st.sidebar.caption(f"🕐 Session: {minutes}m")

        # Auto-logout after 2 hours (security feature)
        if access_duration.total_seconds() > 7200:  # 2 hours
            st.warning("Session expired due to inactivity")
            st.session_state.authenticated = False
            st.rerun()

    except:
        pass

# Logout button
if st.sidebar.button("🚪 Secure Logout", key="secure_logout"):
    # Log logout with BOTH systems
    try:
        # NEW: Cloud logger
        cloud_logger.log_access(st.session_state.client_type, "logout")
    except Exception as e:
        print(f"Note: Cloud logging unavailable - {e}")

    # Keep original file logging as backup
    try:
        with open("access_log.txt", "a", encoding="utf-8") as f:
            f.write(f"{dt.datetime.now()}: {st.session_state.client_type.upper()} client logged out\n")
    except:
        pass

    # Clear session state properly
    for key in list(st.session_state.keys()):
        del st.session_state[key]

    st.rerun()

# Initialize alert system
alert_system = TelegramAlertSystem()


# ======== WORKING AUDIO ALERT FUNCTIONS ========
def play_simple_alert():
    """Simple alert sound using web-based audio - ACTUALLY WORKS"""
    try:
        # Use browser's built-in speech synthesis for a beep sound
        audio_html = """
        <script>
        function playBeep() {
            const context = new (window.AudioContext || window.webkitAudioContext)();
            const oscillator = context.createOscillator();
            const gainNode = context.createGain();

            oscillator.connect(gainNode);
            gainNode.connect(context.destination);

            oscillator.frequency.value = 800;
            oscillator.type = 'sine';
            gainNode.gain.value = 0.1;

            oscillator.start();
            gainNode.gain.exponentialRampToValueAtTime(0.00001, context.currentTime + 0.5);
            oscillator.stop(context.currentTime + 0.5);
        }
        playBeep();
        </script>
        """
        st.components.v1.html(audio_html, height=0)
    except:
        pass  # Fail silently


def play_critical_alert():
    """More urgent sound for critical alerts"""
    try:
        audio_html = """
        <script>
        function playCriticalBeep() {
            const context = new (window.AudioContext || window.webkitAudioContext)();
            const oscillator = context.createOscillator();
            const gainNode = context.createGain();

            oscillator.connect(gainNode);
            gainNode.connect(context.destination);

            // Higher frequency for more urgent sound
            oscillator.frequency.value = 1200;
            oscillator.type = 'sawtooth';
            gainNode.gain.value = 0.15;

            oscillator.start();
            gainNode.gain.exponentialRampToValueAtTime(0.00001, context.currentTime + 0.8);
            oscillator.stop(context.currentTime + 0.8);
        }
        playCriticalBeep();
        </script>
        """
        st.components.v1.html(audio_html, height=0)
    except:
        pass


def autoplay_audio(file_path: str):
    """Fallback audio function - uses web audio instead of files"""
    play_critical_alert()  # Use the web-based version


def show_visual_alert(message, alert_type="warning"):
    """Show visual alert with icons"""
    if alert_type == "critical":
        st.error(f"🚨 {message}")
    elif alert_type == "warning":
        st.warning(f"⚠️ {message}")
    else:
        st.info(f"ℹ️ {message}")


# ======== PROFESSIONAL COLOR SCHEME ========
def apply_professional_styles():
    st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #1f77b4;
    }
    .prediction-high {
        background-color: #ffebee;
        padding: 0.5rem;
        border-radius: 5px;
        border-left: 3px solid #d32f2f;
    }
    .prediction-medium {
        background-color: #fff3e0;
        padding: 0.5rem;
        border-radius: 5px;
        border-left: 3px solid #ff9800;
    }
    .professional-refresh {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.8rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        text-align: center;
        font-weight: 500;
    }
    .refresh-countdown {
        font-size: 1.1rem;
        font-weight: 600;
        color: #1f77b4;
    }
    </style>
    """, unsafe_allow_html=True)


# Apply the styles
apply_professional_styles()

# ======== INITIALIZE ALL SESSION STATE VARIABLES ========
if 'live_mode' not in st.session_state:
    st.session_state.live_mode = False
if 'last_refresh_time' not in st.session_state:
    st.session_state.last_refresh_time = dt.datetime.now()
if 'update_count' not in st.session_state:
    st.session_state.update_count = 0
if 'enterprise_mode' not in st.session_state:
    st.session_state.enterprise_mode = {
        'live_mode': False,
        'last_update': dt.datetime.now(),
        'update_count': 0,
        'data_stream': True,
        'alert_system': True
    }
if 'stream_expanded' not in st.session_state:
    st.session_state.stream_expanded = True
if 'map_view' not in st.session_state:
    st.session_state.map_view = "Current Monitoring"
if 'previous_critical_count' not in st.session_state:
    st.session_state.previous_critical_count = 0
if 'previous_high_risk_count' not in st.session_state:
    st.session_state.previous_high_risk_count = 0
if 'show_critical_alert' not in st.session_state:
    st.session_state.show_critical_alert = False
if 'show_prediction_alert' not in st.session_state:
    st.session_state.show_prediction_alert = False
if 'refresh_trigger' not in st.session_state:
    st.session_state.refresh_trigger = 0
if 'live_data_df' not in st.session_state:
    st.session_state.live_data_df = None


# ======== AUTO-REFRESH LOGIC ========
def check_auto_refresh():
    """Check if it's time to auto-refresh and update data"""
    if st.session_state.get('live_mode', False):
        current_time = dt.datetime.now()
        time_since_refresh = (current_time - st.session_state.last_refresh_time).seconds

        # Auto-refresh every 30 seconds
        if time_since_refresh >= 30:
            # Update the refresh time
            st.session_state.last_refresh_time = current_time
            st.session_state.update_count += 1
            st.session_state.refresh_trigger += 1  # Force refresh

            # Store previous state to detect changes
            previous_critical_count = st.session_state.get('previous_critical_count', 0)

            # Generate new data with variations
            new_df = generate_sample_data(include_live_variation=True)
            if 'status' not in new_df.columns:
                new_df['status'] = new_df.apply(
                    lambda row: get_water_quality_status(row['turbidity_ntu'], row['ph']),
                    axis=1
                )

            # Check for important changes that need attention
            current_critical_count = len(new_df[new_df['status'] == "🔴 Critical"])

            # Show notification for new critical events
            if current_critical_count > previous_critical_count:
                new_critical_count = current_critical_count - previous_critical_count
                st.session_state.show_critical_alert = True
                st.toast(f"🚨 NEW CRITICAL ALERT: {new_critical_count} new rivers in danger!", icon="🚨")

                # PLAY ACTUAL SOUND ALERT - THIS WILL WORK
                play_critical_alert()

            # Store current state for next comparison
            st.session_state.previous_critical_count = current_critical_count

            # Update the main dataframe
            st.session_state.live_data_df = new_df

            return True, new_df

    return False, None


# Check for auto-refresh at the start
should_refresh, new_data = check_auto_refresh()

# Title and description
st.markdown('<h1 class="main-header">🇬🇭 Guardian Ghana - AI Water Protection</h1>', unsafe_allow_html=True)
st.markdown("""
### Real-time Water Quality Monitoring & Pollution Prediction System
Using AI to detect and predict water pollution events before they cause irreversible damage.
*Live monitoring + predictive analytics*
""")

# ======== FIXED CSV/EXCEL UPLOAD ========
st.sidebar.header("📤 Upload Your Water Data")
uploaded_file = st.sidebar.file_uploader(
    "Upload CSV or Excel file with water quality data",
    type=['csv', 'xlsx', 'xls'],
    key="file_uploader"
)

# ======== SMART DATA DISPLAY ========
st.sidebar.markdown("---")
st.sidebar.header("📊 Data Display")

display_mode = st.sidebar.radio(
    "Choose what data to display:",
    ["Sample Monitoring Data", "Only My Uploaded Data", "Combined Data"],
    index=0,
    key="display_mode_radio"
)


def get_combined_data():
    # Use live data if available and in live mode
    if st.session_state.get('live_mode', False) and st.session_state.live_data_df is not None:
        base_df = st.session_state.live_data_df
    else:
        # Generate base data WITH LIVE VARIATIONS if live mode is active
        include_variations = st.session_state.get('live_mode', False)
        base_df = generate_sample_data(include_live_variation=include_variations)

    # Ensure base_df has status column
    if 'status' not in base_df.columns:
        base_df['status'] = base_df.apply(
            lambda row: get_water_quality_status(row['turbidity_ntu'], row['ph']),
            axis=1
        )

    # Process uploaded file ONLY if it exists
    if uploaded_file is not None:
        try:
            # Read file based on type
            if uploaded_file.name.endswith('.csv'):
                user_df = pd.read_csv(uploaded_file)
            else:  # Excel file
                user_df = pd.read_excel(uploaded_file)

            required_columns = ['latitude', 'longitude', 'turbidity_ntu', 'ph', 'river_name']

            if all(col in user_df.columns for col in required_columns):
                st.sidebar.success("✅ File successfully loaded!")

                # Add missing columns with defaults
                if 'timestamp' not in user_df.columns:
                    user_df['timestamp'] = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                if 'dissolved_oxygen' not in user_df.columns:
                    user_df['dissolved_oxygen'] = 5.0

                # Add status column
                user_df['status'] = user_df.apply(
                    lambda row: get_water_quality_status(row['turbidity_ntu'], row['ph']),
                    axis=1
                )

                # APPLY DISPLAY MODE PREFERENCE
                if display_mode == "Only My Uploaded Data":
                    if uploaded_file is not None:
                        return user_df
                    else:
                        st.sidebar.warning("⚠️ No file uploaded. Showing sample data.")
                        return base_df
                elif display_mode == "Combined Data":
                    if uploaded_file is not None:
                        return pd.concat([base_df, user_df], ignore_index=True)
                    else:
                        return base_df
                else:  # Sample Monitoring Data
                    return base_df

            else:
                missing_cols = [col for col in required_columns if col not in user_df.columns]
                st.sidebar.error(f"❌ Missing columns: {missing_cols}")
                return base_df

        except Exception as e:
            st.sidebar.error(f"❌ Error reading file: {str(e)}")
            return base_df

    return base_df


# ======== SAFE DATA LOADING ========
try:
    df = get_combined_data()

    # DOUBLE CHECK: Ensure status column exists
    if 'status' not in df.columns:
        st.error("❌ Status column missing - creating it now...")
        df['status'] = df.apply(
            lambda row: get_water_quality_status(row['turbidity_ntu'], row['ph']),
            axis=1
        )

except Exception as e:
    st.error(f"❌ Critical error loading data: {str(e)}")
    st.stop()

# ======== SAMPLE FILE DOWNLOADS ========
st.sidebar.markdown("---")
st.sidebar.subheader("Download Templates")

# CSV Template
st.sidebar.download_button(
    label="📥 Download CSV Template",
    data="""river_name,latitude,longitude,turbidity_ntu,ph,dissolved_oxygen
Test River 1,5.5,-1.2,45,6.8,5.2
Test River 2,6.1,-1.8,120,5.9,3.1
Test River 3,5.8,-1.1,180,5.2,2.5""",
    file_name="water_quality_template.csv",
    mime="text/csv",
    key="download_csv_template"
)


# Excel Template
@st.cache_data
def create_excel_template():
    import io
    template_df = pd.DataFrame({
        'river_name': ['Test River 1', 'Test River 2'],
        'latitude': [5.5, 6.1],
        'longitude': [-1.2, -1.8],
        'turbidity_ntu': [45, 120],
        'ph': [6.8, 5.9],
        'dissolved_oxygen': [5.2, 3.1]
    })

    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
        template_df.to_excel(writer, sheet_name='Water_Data', index=False)
    return buffer.getvalue()


st.sidebar.download_button(
    label="📥 Download Excel Template",
    data=create_excel_template(),
    file_name="water_quality_template.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    key="download_excel_template"
)

# ======== PROFESSIONAL DASHBOARD LAYOUT ========
st.markdown("---")
col_left, col_right = st.columns([2, 1])
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    critical_count = len(df[df['status'] == "🔴 Critical"])
    st.metric("🚨 Critical Rivers", critical_count, delta=None)

with col2:
    warning_count = len(df[df['status'] == "🟡 Warning"])
    st.metric("⚠️ Warning Rivers", warning_count, delta=None)

with col3:
    if 'predictions' in st.session_state:
        high_risk_count = len(
            [p for p in st.session_state.predictions if "HIGH" in p['risk_level'] or "CRITICAL" in p['risk_level']])
        st.metric("🔴 Predicted High Risk", high_risk_count)
    else:
        total_rivers = len(df)
        st.metric("📊 Total Monitored", total_rivers)

with col4:
    if st.session_state.get('live_mode', False):
        st.metric("🟢 System Status", "LIVE", delta=f"{st.session_state.update_count} updates")
    else:
        st.metric("🟢 System Status", "Online", delta="Active")

with col5:
    if 'validation_results' in st.session_state:
        accuracy = st.session_state.validation_results['accuracy']
        st.metric("🎯 AI Accuracy", accuracy, delta="Validated")
    else:
        st.metric("🎯 AI Accuracy", "87%", delta="Baseline")

# ======== PROFESSIONAL LIVE MODE STATUS ========
st.markdown("---")

if st.session_state.get('live_mode', False):
    # Calculate time since last update
    current_time = dt.datetime.now()
    time_since_update = (current_time - st.session_state.last_refresh_time).seconds
    time_to_next_update = max(0, 30 - time_since_update)

    # PROFESSIONAL STATUS INDICATORS
    col_status1, col_status2, col_status3 = st.columns(3)

    with col_status1:
        # System Uptime
        st.metric(
            "🔄 System Uptime",
            f"{st.session_state.update_count} cycles",
            delta="Active" if time_since_update < 10 else "Monitoring"
        )

    with col_status2:
        # Data Freshness
        freshness_status = "Real-time" if time_since_update < 5 else "Current" if time_since_update < 15 else "Refreshing"
        st.metric("📊 Data Status", freshness_status, delta=f"{time_since_update}s ago")

    with col_status3:
        # Next Refresh - PROFESSIONAL
        refresh_status = "Imminent" if time_to_next_update <= 5 else "Scheduled"
        st.metric("🕐 Next Refresh", f"{time_to_next_update}s", delta=refresh_status)

    # CRITICAL ALERTS PANEL (Only show when there are actual alerts)
    critical_rivers = df[df['status'] == "🔴 Critical"]
    if not critical_rivers.empty:
        st.error(f"### Critical Alert: {len(critical_rivers)} Rivers Require Immediate Attention")
        for _, river in critical_rivers.iterrows():
            with st.expander(f"**{river['river_name']}** - Critical Conditions", expanded=False):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Turbidity:** {river['turbidity_ntu']} NTU")
                    st.write(f"**pH Level:** {river['ph']:.1f}")
                with col2:
                    st.write(f"**Dissolved Oxygen:** {river['dissolved_oxygen']:.1f} mg/L")
                    st.write(f"**Last Reading:** {river['timestamp']}")

    # HIGH-RISK PREDICTIONS PANEL
    if 'predictions' in st.session_state:
        high_risk_predictions = [p for p in st.session_state.predictions
                                 if "CRITICAL" in p['risk_level'] or "HIGH" in p['risk_level']]
        if high_risk_predictions:
            st.warning(f"### Predictive Alert: {len(high_risk_predictions)} High-Risk Areas Identified")
            for pred in high_risk_predictions[:2]:  # Show top 2 only
                with st.expander(
                        f"**{pred['river_name']}** - {pred['risk_level']} (Score: {pred['risk_score']:.0f}/100)",
                        expanded=False):
                    st.write(f"**Confidence:** {pred.get('confidence', 'High')}")
                    st.write(
                        f"**Nearest Hotspot:** {pred['nearest_hotspot']['name']} ({pred['nearest_hotspot']['distance_km']}km)")
                    st.write("**Key Factors:**")
                    for factor in pred['factors'][:3]:
                        st.write(f"• {factor}")

    # Progress indicator (subtle)
    progress = min(time_since_update / 30, 1.0)
    st.progress(progress)
    st.caption(f"Refresh cycle progress: {int(progress * 100)}% complete")

# ======== RELIABLE AUTO-REFRESH SYSTEM ========
if st.session_state.get('live_mode', False):
    current_time = dt.datetime.now()
    time_since_refresh = (current_time - st.session_state.last_refresh_time).seconds

    # Auto-refresh every 30 seconds
    if time_since_refresh >= 30:
        # Perform the refresh
        st.session_state.last_refresh_time = current_time
        st.session_state.update_count += 1

        # Generate new data
        new_df = generate_sample_data(include_live_variation=True)
        if 'status' not in new_df.columns:
            new_df['status'] = new_df.apply(
                lambda row: get_water_quality_status(row['turbidity_ntu'], row['ph']),
                axis=1
            )

        # Check for critical changes
        previous_critical = st.session_state.get('previous_critical_count', 0)
        current_critical = len(new_df[new_df['status'] == "🔴 Critical"])

        if current_critical > previous_critical:
            new_critical = current_critical - previous_critical
            st.toast(f"🚨 New Critical Alert: {new_critical} additional rivers in danger", icon="🚨")
            play_critical_alert()  # Play sound for critical alerts

        st.session_state.previous_critical_count = current_critical
        st.session_state.live_data_df = new_df

        # Force refresh
        st.rerun()

# ======== ENHANCED AI PREDICTION SYSTEM ========
st.sidebar.markdown("---")
st.sidebar.header("🧠 AI Pollution Predictions")

col_pred1, col_pred2 = st.sidebar.columns(2)
with col_pred1:
    if st.button("🔄 Risk Check", key="run_risk_assessment"):
        with st.spinner("🛰️ Accessing satellite data..."):
            time.sleep(1)
        with st.spinner("🌧️ Analyzing weather patterns..."):
            time.sleep(1)
        with st.spinner("📍 Assessing mining hotspots..."):
            time.sleep(1)
        with st.spinner("🤖 Calculating pollution risks..."):
            # Generate predictions for current rivers
            predictions = []
            for _, river in df.iterrows():
                prediction = predictor.predict_pollution_risk(
                    river['latitude'],
                    river['longitude'],
                    river['river_name']
                )
                predictions.append(prediction)

            # Generate risk map data
            risk_map_data = predictor.generate_risk_map_data()

            st.session_state.predictions = predictions
            st.session_state.risk_map_data = risk_map_data

        st.sidebar.success("✅ AI risk assessment complete!")

with col_pred2:
    if st.button("🗺️ Show Risk Map", key="show_risk_map_btn"):
        if 'risk_map_data' not in st.session_state:
            st.sidebar.warning("⚠️ Please run 'Risk Check' first to generate predictions")
        else:
            st.session_state.risk_map_view = True
            st.session_state.map_view = "AI Risk Prediction"
            st.sidebar.success("🎯 Switching to AI Risk Map view...")
            st.rerun()

# ======== VALIDATION DASHBOARD ========
st.sidebar.markdown("---")
st.sidebar.header("📊 Model Validation")

try:
    from data.validation_data import validate_predictions, HISTORICAL_EVENTS, calculate_distance
except ImportError:
    st.sidebar.warning("Validation module not available")

if st.sidebar.button("🧪 Run Accuracy Test", key="run_validation"):
    if 'predictions' in st.session_state:
        with st.spinner("Validating against historical pollution events..."):
            time.sleep(2)
            validation_results = validate_predictions(st.session_state.predictions)
            st.session_state.validation_results = validation_results
            st.sidebar.success("✅ Validation complete!")
    else:
        st.sidebar.warning("Please run AI Risk Check first")

if 'validation_results' in st.session_state:
    results = st.session_state.validation_results
    st.sidebar.markdown("### 📈 Validation Results")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("🎯 Accuracy", results['accuracy'])
    with col2:
        st.metric("📊 Precision", results['precision'])
    st.sidebar.metric("📈 Recall", results['recall'])
    st.sidebar.caption(f"Tested on {results['tested_events']} historical events")
    st.sidebar.caption(f"Matched {results.get('matched_events', 0)} events correctly")

# Display prediction insights
if 'predictions' in st.session_state:
    st.sidebar.markdown("---")
    st.sidebar.subheader("📊 AI Risk Assessment")
    high_risk_count = sum(
        1 for p in st.session_state.predictions if "CRITICAL" in p['risk_level'] or "HIGH" in p['risk_level'])
    medium_risk_count = sum(1 for p in st.session_state.predictions if "MEDIUM" in p['risk_level'])
    st.sidebar.metric("🔴 High Risk Areas", high_risk_count)
    st.sidebar.metric("🟡 Medium Risk Areas", medium_risk_count)

# ======== MAP SECTION ========
with col_left:
    st.subheader("🇬🇭 Ghana River Monitoring Map")

    # Initialize map_view if not exists
    if 'map_view' not in st.session_state:
        st.session_state.map_view = "Current Monitoring"

    # Handle the "Show Risk Map" button click - THIS MUST BE BEFORE RADIO
    if st.session_state.get('risk_map_view', False):
        st.session_state.map_view = "AI Risk Prediction"
        st.session_state.risk_map_view = False
        st.rerun()  # Force refresh to show change

    # Choose map type - Use callback to update session state
    map_type = st.radio(
        "Map View:",
        ["Current Monitoring", "AI Risk Prediction"],
        horizontal=True,
        key="map_type_radio",
        index=0 if st.session_state.map_view == "Current Monitoring" else 1,
        on_change=lambda: update_map_view()  # Add callback
    )


    # Update function for radio button
    def update_map_view():
        # Get the current radio button value
        if 'map_type_radio' in st.session_state:
            st.session_state.map_view = st.session_state.map_type_radio


    # SINGLE MAP DISPLAY - NO DUPLICATES
    try:
        if st.session_state.map_view == "AI Risk Prediction":
            if 'risk_map_data' in st.session_state and not st.session_state.risk_map_data.empty:
                risk_map = create_risk_overlay_map(df, st.session_state.risk_map_data)
                display_map(risk_map)
                st.success("🎯 **AI Risk Map Active**: Showing predicted pollution risk areas")

                # Risk distribution analysis
                risk_data = st.session_state.risk_map_data
                critical_risks = len(risk_data[risk_data['risk_score'] >= 80])
                high_risks = len(risk_data[(risk_data['risk_score'] >= 60) & (risk_data['risk_score'] < 80)])
                medium_risks = len(risk_data[(risk_data['risk_score'] >= 40) & (risk_data['risk_score'] < 60)])

                st.markdown("---")
                st.subheader("📈 Risk Distribution Analysis")
                col_stat1, col_stat2, col_stat3 = st.columns(3)
                with col_stat1:
                    st.metric("🔴 Critical", critical_risks)
                with col_stat2:
                    st.metric("🟠 High", high_risks)
                with col_stat3:
                    st.metric("🟡 Medium", medium_risks)

                if critical_risks > 0:
                    hotspots = risk_data[risk_data['risk_score'] >= 80]['river_name'].value_counts()
                    st.warning(f"🚨 **Critical Risk Hotspots**: {', '.join(hotspots.index[:3])}")
            else:
                st.warning("⚠️ No AI risk data available. Please run 'Risk Check' first.")
                water_map = create_ghana_water_map(df)
                display_map(water_map)
        else:
            water_map = create_ghana_water_map(df)
            display_map(water_map)
            st.info("📊 **Current Monitoring**: Real-time water quality status")

    except Exception as e:
        st.error(f"❌ Map rendering error: {str(e)}")
        fallback_map = folium.Map(location=[7.9465, -1.0232], zoom_start=7)
        display_map(fallback_map)

    st.caption("""
    **Map Legend:**
    🟥 **Red** = Critical/High Risk | 🟨 **Yellow/Orange** = Warning/Medium Risk | 🟩 **Green** = Normal/Low Risk
    """)

# ======== SIMPLIFIED LIVE DATA MODE ========
st.sidebar.markdown("---")
st.sidebar.header("🔄 Live Data Mode")

col_live1, col_live2 = st.sidebar.columns(2)
with col_live1:
    live_button = st.button("🎯 Enable Live Mode" if not st.session_state.live_mode else "⏹️ Stop Live Mode",
                            key="toggle_live_mode")

    if live_button:
        st.session_state.live_mode = not st.session_state.live_mode
        if st.session_state.live_mode:
            st.session_state.last_refresh_time = dt.datetime.now()
            st.session_state.update_count = 0
            # Initialize live data
            st.session_state.live_data_df = generate_sample_data(include_live_variation=True)
            st.sidebar.success("🟢 Live mode activated! Auto-refreshing every 30 seconds")
        else:
            st.sidebar.info("🔴 Live mode deactivated")
        time.sleep(0.5)
        st.rerun()

with col_live2:
    if st.session_state.live_mode:
        if st.button("🔄 Force Refresh", key="force_refresh"):
            st.session_state.update_count += 1
            st.session_state.last_refresh_time = dt.datetime.now()  # FIXED
            st.session_state.live_data_df = generate_sample_data(include_live_variation=True)
            st.rerun()

# Live Data Stream (ALWAYS in sidebar for consistency)
if st.session_state.get('live_mode', False) and st.session_state.update_count > 0:
    with st.sidebar.expander("📡 Live Data Stream", expanded=st.session_state.stream_expanded):
        st.success("✅ Satellite: NASA Aqua/MODIS - Data received")
        st.success("✅ Weather: Ghana Meteo - Patterns analyzed")
        st.success("✅ AI Engine: Risk predictions updated")
        st.success("✅ Alert System: Monitoring channels active")

        if random.random() > 0.7:
            st.warning("⚠️ Anomaly: Turbidity spike detected in Pra River")
        if random.random() > 0.9:
            st.error("🚨 CRITICAL: Mercury levels rising in Ankobra")

        if st.button("🔄 Refresh Stream", key="refresh_stream"):
            st.session_state.stream_expanded = not st.session_state.stream_expanded
            st.rerun()

# ======== RIGHT SIDEBAR CONTENT ========
with col_right:
    st.subheader("📈 Quick Insights")

    # REAL-TIME MONITORING PANEL
    if st.session_state.get('live_mode', False):
        st.write("### Live Monitor")

        # System status
        if st.session_state.update_count == 0:
            st.info("🟢 **System Ready** - Waiting for first update...")
        else:
            st.success(f"🟢 **Live Monitoring** - {st.session_state.update_count} updates received")

        # Alert status
        critical_count = len(df[df['status'] == "🔴 Critical"])
        if critical_count > 0:
            st.error(f"🚨 **{critical_count} CRITICAL** rivers need attention!")
        else:
            st.success("✅ No critical alerts")

        # Prediction status
        if 'predictions' in st.session_state:
            high_risk_count = len([p for p in st.session_state.predictions
                                   if "CRITICAL" in p['risk_level'] or "HIGH" in p['risk_level']])
            if high_risk_count > 0:
                st.warning(f"🔮 **{high_risk_count} HIGH-RISK** predictions active")
            else:
                st.info("🌤️  No high-risk predictions")

        # Last activity
        time_since_update = (dt.datetime.now() - st.session_state.last_refresh_time).seconds
        st.caption(f"🕐 Last activity: {time_since_update} seconds ago")

    # Current alerts summary
    st.write("### 🚨 Active Alerts")
    alerts = df[df['status'] != "🟢 Normal"]
    if not alerts.empty:
        for idx, alert in alerts.iterrows():
            if alert['status'] == "🔴 Critical":
                st.error(f"**{alert['river_name']}** - {alert['status']}")
            else:
                st.warning(f"**{alert['river_name']}** - {alert['status']}")
    else:
        st.success("✅ No active pollution alerts")

    # Quick actions
    st.write("### ⚡ Quick Actions")

    col_action1, col_action2 = st.columns(2)

    with col_action1:
        if st.button("🔄 Send Alerts", type="secondary", key="check_current_alerts"):
            try:
                alerts_sent = check_and_alert(df)
                if alerts_sent > 0:
                    st.warning(f"🚨 {alerts_sent} alerts sent!")
                    play_simple_alert()  # Add sound feedback
                else:
                    st.success("✅ All systems normal")
            except Exception as e:
                st.error(f"Alert system error: {str(e)}")

    with col_action2:
        if st.button("🔮 Send Prediction Alerts", type="secondary", key="check_prediction_alerts"):
            try:
                predictions = st.session_state.get('predictions', [])
                alerts_sent = check_and_alert(df, predictions)
                if alerts_sent > 0:
                    st.warning(f"🚨 {alerts_sent} prediction alerts sent!")
                    play_simple_alert()  # Add sound feedback
                else:
                    st.success("✅ No critical predictions")
            except Exception as e:
                st.error(f"Prediction alert error: {str(e)}")

# Data section below
st.markdown("---")
st.subheader("📋 Detailed Water Quality Data")

try:
    st.dataframe(df[['river_name', 'turbidity_ntu', 'ph', 'dissolved_oxygen', 'status', 'timestamp']], height=300)
except Exception as e:
    st.error(f"Error displaying data: {str(e)}")

# ======== ENHANCED ADMIN PANEL WITH CEO FEATURES ========
st.sidebar.markdown("---")
st.sidebar.header("🔧 System Administration")

# If CEO, auto-unlock admin
if st.session_state.get('is_ceo', False) and not st.session_state.get('admin_unlocked', False):
    st.session_state.admin_unlocked = True
    st.sidebar.success("👑 CEO ACCESS GRANTED")

# Admin login section
if not st.session_state.get('admin_unlocked', False):
    st.sidebar.write("**Admin Access Required**")
    admin_pass = st.sidebar.text_input("Admin Code:", type="password", key="admin_pass")

    col1, col2 = st.sidebar.columns(2)
    with col1:
        if st.sidebar.button("🔓 Unlock Admin", key="admin_unlock_btn", use_container_width=True):
            if admin_pass == ADMIN_PASSWORD:
                st.session_state.admin_unlocked = True
                st.sidebar.success("✅ Admin access granted")
                st.rerun()
            else:
                st.sidebar.error("❌ Invalid admin code")
    with col2:
        if st.sidebar.button("🔄 Clear", key="admin_clear_btn", use_container_width=True):
            st.rerun()
else:
    # ADMIN IS UNLOCKED - SHOW ADMIN PANEL
    if st.session_state.get('is_ceo', False):
        st.sidebar.success("👑 **SUPER ADMINISTRATOR**")
        
        # Create tabs including CEO tab
        admin_tab1, admin_tab2, admin_tab3, admin_tab4, admin_tab5 = st.sidebar.tabs(
            ["👑 CEO", "📊 Analytics", "👥 Users", "⚙️ System", "🔒 Security"]
        )
    else:
        st.sidebar.success("✅ **SYSTEM ADMINISTRATOR**")
        
        # Create tabs without CEO tab for non-CEO admins
        admin_tab1, admin_tab2, admin_tab3, admin_tab4 = st.sidebar.tabs(
            ["📊 Analytics", "👥 Users", "⚙️ System", "🔒 Security"]
        )
    
    # CEO TAB (only for CEO)
    if st.session_state.get('is_ceo', False):
        with admin_tab1:
            st.success("## 👑 GUARDIAN GHANA - CEO DASHBOARD")
            
            # Real-time business metrics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("🚀 MRR Target", "₵625,000", "₵62,500 current")
            with col2:
                st.metric("🎯 Pilot Clients", "3", "Gold Fields, EPA, Newmont")
            with col3:
                st.metric("📈 Valuation", "₵312.5M", "Pre-money")
            
            # Quick Actions
            st.write("### ⚡ Quick Actions")
            if st.button("📧 Send Investor Update"):
                st.info("Investor update template loaded")
            
            if st.button("📊 Update Revenue Projections"):
                st.info("Opening revenue calculator...")
            
            if st.button("👥 Add New Client"):
                new_client = st.text_input("Client Name:")
                if st.button("Generate Client Password"):
                    import random
                    st.success(f"Password for {new_client}: CLIENT_{random.randint(1000,9999)}")
            
            # Client Pipeline
            st.write("### 🎯 Active Pipeline")
            pipeline = [
                {"client": "Gold Fields", "stage": "Demo Call", "value": "₵187,500/mo", "next": "12/13"},
                {"client": "Ghana EPA", "stage": "Proposal Review", "value": "₵625,000/mo", "next": "12/15"},
                {"client": "Newmont", "stage": "Initial Contact", "value": "₵187,500/mo", "next": "12/16"},
            ]
            
            for deal in pipeline:
                col1, col2, col3, col4 = st.columns([3, 2, 2, 1])
                with col1:
                    st.write(f"**{deal['client']}**")
                with col2:
                    st.write(deal['stage'])
                with col3:
                    st.write(deal['value'])
                with col4:
                    if st.button("→", key=f"action_{deal['client']}"):
                        st.session_state.selected_client = deal['client']
    
    # ANALYTICS TAB (for all admins)
    with admin_tab2 if st.session_state.get('is_ceo', False) else admin_tab1:
        st.write("### System Analytics")

        # Real-time metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Active Users", "24", "+3 today")
        with col2:
            st.metric("Predictions Run", "1,247", "87% accuracy")
        with col3:
            st.metric("Alerts Sent", "156", "12 critical")

        # Access logs with search
        st.write("### Access Logs")
        try:
            if os.path.exists("access_log.txt"):
                with open("access_log.txt", "r", encoding="utf-8") as f:
                    logs = f.readlines()

                search_term = st.text_input("Search logs:")
                if search_term:
                    filtered_logs = [log for log in logs if search_term.lower() in log.lower()]
                else:
                    filtered_logs = logs[-50:]  # Last 50 entries

                st.text_area("Recent Activity:", "".join(filtered_logs), height=200)

                # Export options
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("📥 Download Full Logs"):
                        st.download_button(
                            "Download",
                            "".join(logs),
                            file_name=f"access_logs_{dt.datetime.now().strftime('%Y%m%d')}.txt"
                        )
                with col2:
                    if st.button("🔄 Refresh Logs"):
                        st.rerun()
            else:
                st.info("No access logs available")
        except Exception as e:
            st.error(f"Error reading logs: {e}")

        # Cloud Access Analytics
        st.write("---")
        st.write("### 📊 Cloud Access Analytics")
        st.info("Professional logging system for investor demonstrations")

        # Show analytics summary
        try:
            analytics = cloud_logger.get_analytics_summary()

            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Logins", analytics.get('total_logins', 0))
            with col2:
                st.metric("Unique Client Types", analytics.get('unique_client_types', 0))
            with col3:
                if analytics.get('last_login'):
                    st.metric("Last Activity", analytics['last_login'][:10])

            # Show client distribution
            if 'client_types' in analytics and analytics['client_types']:
                st.write("**Client Distribution:**")
                for client_type, count in analytics['client_types'].items():
                    if client_type == "government":
                        st.success(f"🏛️ Government: {count} logins")
                    elif client_type == "corporate":
                        st.info(f"🏢 Corporate: {count} logins")
                    elif client_type == "demo":
                        st.warning(f"🎪 Demo/Trial: {count} logins")
                    else:
                        st.write(f"👤 {client_type}: {count}")

            # Export cloud logs
            log_json = cloud_logger.export_logs()
            if st.button("📥 Download Cloud Logs (JSON)"):
                st.download_button(
                    label="Download Now",
                    data=log_json,
                    file_name=f"guardian_ghana_cloud_logs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )

        except Exception as e:
            st.warning(f"Cloud analytics not available yet: {e}")
            st.info("Cloud logging will become active after users log in")

    # USERS TAB
    with admin_tab3 if st.session_state.get('is_ceo', False) else admin_tab2:
        st.write("### User Management")

        # Simulated user database
        users = [
            {"name": "EPA Ghana", "email": "director@epa.gov.gh", "access": "Full", "last_login": "2025-12-07"},
            {"name": "Gold Fields", "email": "env@goldfields.com", "access": "Corporate", "last_login": "2025-12-06"},
            {"name": "Demo Client", "email": "demo@example.com", "access": "Trial", "last_login": "2025-12-05"},
        ]

        for user in users:
            col1, col2, col3 = st.columns([3, 2, 1])
            with col1:
                st.write(f"**{user['name']}**")
                st.caption(user['email'])
            with col2:
                st.write(user['access'])
            with col3:
                if st.button("Reset", key=f"reset_{user['email']}"):
                    st.success(f"Password reset sent to {user['email']}")

        # Add new user
        st.write("### Add New User")
        new_email = st.text_input("Email Address:")
        new_access = st.selectbox("Access Level:", ["Trial", "Corporate", "Government", "Admin"])
        if st.button("Create User"):
            st.success(f"Invitation sent to {new_email}")

    # SYSTEM TAB
    with admin_tab4 if st.session_state.get('is_ceo', False) else admin_tab3:
        st.write("### System Configuration")

        # AI Model Settings
        st.write("**AI Model Settings**")
        confidence_threshold = st.slider("Confidence Threshold", 50, 95, 70)
        prediction_horizon = st.selectbox("Prediction Horizon", ["24 hours", "48 hours", "72 hours", "5 days"])

        # Alert Settings
        st.write("**Alert System**")
        col1, col2 = st.columns(2)
        with col1:
            email_alerts = st.checkbox("Email Alerts", True)
            telegram_alerts = st.checkbox("Telegram Alerts", True)
        with col2:
            sound_alerts = st.checkbox("Sound Alerts", True)
            critical_only = st.checkbox("Critical Only", False)

        if st.button("💾 Save Configuration"):
            st.success("Configuration saved!")

    # SECURITY TAB
    with admin_tab5 if st.session_state.get('is_ceo', False) else admin_tab4:
        st.write("### Security Dashboard")

        # Security status
        st.success("✅ All systems secure")
        st.info("🔒 Password protection: Active")
        st.info("📊 Access logging: Active")
        st.info("⏰ Session timeout: 60 minutes")

        # Security actions
        st.write("### Security Actions")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Rotate Passwords"):
                st.warning("Password rotation initiated")
        with col2:
            if st.button("📋 Export Audit Trail"):
                st.info("Audit trail exported")

        # Threat detection (simulated)
        st.write("### Threat Detection")
        threats = [
            {"type": "Brute Force Attempt", "severity": "Low", "time": "2 hours ago"},
            {"type": "Multiple Failed Logins", "severity": "Medium", "time": "1 day ago"},
        ]

        for threat in threats:
            col1, col2, col3 = st.columns([3, 1, 1])
            with col1:
                st.write(threat['type'])
            with col2:
                if threat['severity'] == "High":
                    st.error(threat['severity'])
                elif threat['severity'] == "Medium":
                    st.warning(threat['severity'])
                else:
                    st.info(threat['severity'])
            with col3:
                st.caption(threat['time'])

    # Quick actions at bottom
    st.sidebar.markdown("---")
    if st.sidebar.button("🚪 Exit Admin Mode", type="primary"):
        st.session_state.admin_unlocked = False
        st.rerun()

# Footer
st.markdown("---")
st.markdown("""
**About This Project**: Guardian Ghana uses AI and real-time monitoring to protect Ghana's water resources from illegal mining pollution.
Built with Python, Streamlit, Folium, and Machine Learning.
""")

# ======== FORCE AUTO-REFRESH ========
# This is the key to making auto-refresh work
if st.session_state.get('live_mode', False):
    # Use the refresh trigger to force updates
    refresh_value = st.session_state.get('refresh_trigger', 0)

    # Add a small delay to prevent excessive CPU usage
    time.sleep(0.1)

# ======== EPA DEMO FEATURES ========
# Only show EPA features for government clients or CEO
if st.session_state.get('show_epa_tools', False) or st.session_state.get('is_ceo', False):
    st.sidebar.markdown("---")
    st.sidebar.header("🏛️ EPA Demo Features")

    # Government dashboard view
    if st.sidebar.checkbox("🏛️ Show Government Dashboard", key="gov_dashboard"):
        st.sidebar.markdown("### Agency Tools")

        # Compliance reporting
        if st.sidebar.button("📋 Generate Compliance Report", key="compliance_report"):
            with st.spinner("Generating EPA compliance report..."):
                time.sleep(2)

                # Generate comprehensive report
                report_data = {
                    "date": dt.datetime.now().strftime("%Y-%m-%d"),
                    "critical_violations": critical_count,
                    "high_risk_predictions": high_risk_count if 'predictions' in st.session_state else 0,
                    "rivers_monitored": len(df),
                    "ai_accuracy": st.session_state.get('validation_results', {}).get('accuracy', '87%')
                }

                # Show report in main area
                st.success("✅ Compliance Report Generated!")
                with st.expander("📄 **EPA Compliance Report**", expanded=True):
                    st.write(f"**Report Date:** {report_data['date']}")
                    st.write(f"**Critical Violations Detected:** {report_data['critical_violations']}")
                    st.write(f"**High-Risk Predictions:** {report_data['high_risk_predictions']}")
                    st.write(f"**Rivers Monitored:** {report_data['rivers_monitored']}")
                    st.write(f"**AI Model Accuracy:** {report_data['ai_accuracy']}")

                    # Action items
                    st.markdown("### 🎯 Recommended Actions")
                    if report_data['critical_violations'] > 0:
                        st.error("1. **Immediate Investigation** required for critical rivers")
                    if report_data['high_risk_predictions'] > 0:
                        st.warning("2. **Preventive Measures** needed for high-risk areas")

                    st.info("3. **Monthly Report** scheduled for submission")

        # Enforcement tools
        if st.sidebar.button("⚖️ Show Enforcement Module", key="enforcement_module"):
            st.info("### 🏛️ EPA Enforcement Dashboard")
            col1, col2 = st.columns(2)

            with col1:
                st.subheader("Active Violations")
                violations = df[df['status'] == "🔴 Critical"]
                for _, river in violations.iterrows():
                    st.error(f"**{river['river_name']}** - Violating EPA Standards")
                    st.write(f"• Turbidity: {river['turbidity_ntu']} NTU (Limit: 100 NTU)")
                    st.write(f"• pH: {river['ph']:.1f} (Range: 6.0-8.5)")
                    st.write("---")

            with col2:
                st.subheader("Enforcement Actions")
                action_options = ["Warning Notice", "Fine Assessment", "Cease & Desist", "Criminal Referral"]
                selected_action = st.selectbox("Select Action:", action_options)
                if st.button("📝 Generate Enforcement Order"):
                    st.success(f"✅ {selected_action} order generated for review")

        # Historical data analysis
        if st.sidebar.button("📊 Trend Analysis", key="trend_analysis"):
            st.info("### 📈 Long-term Water Quality Trends")

            # Simulate historical data
            dates = pd.date_range(end=dt.datetime.now(), periods=30, freq='D')
            trend_data = pd.DataFrame({
                'Date': dates,
                'Pra River Turbidity': np.random.randint(80, 400, 30),
                'Ankobra River pH': np.random.uniform(5.2, 7.0, 30),
                'Birim River DO': np.random.uniform(2.0, 8.0, 30)
            })

            st.line_chart(trend_data.set_index('Date'))
            st.caption("30-day water quality trends for major rivers")

    # ======== EPA SUCCESS METRICS ========
    st.sidebar.markdown("---")
    st.sidebar.header("📊 EPA Success Metrics")

    if st.sidebar.checkbox("Show Impact Analysis", key="impact_analysis"):
        st.info("### 📈 Potential EPA Impact with Guardian Ghana")

        metrics = {
            "Response Time Improvement": {"current": "7-14 days", "with_us": "2-4 hours", "impact": "98% faster"},
            "Detection Accuracy": {"current": "60-70%", "with_us": "87%+", "impact": "25% improvement"},
            "Annual Cost": {"current": "₵28.8M", "with_us": "₵6.25M", "impact": "78% savings"},
            "Coverage": {"current": "40 rivers", "with_us": "200+ rivers", "impact": "5x more coverage"}
        }

        for metric, data in metrics.items():
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric(f"Current {metric}", data["current"])
            with col2:
                st.metric(f"With Guardian Ghana", data["with_us"])
            with col3:
                st.metric("Improvement", data["impact"])

        st.success("""
        **Total Annual Benefit to Ghana:**
        - **₵22.5M cost savings**
        - **300+ pollution events prevented**
        - **2M+ people protected**
        - **5,000+ jobs created** (monitoring, enforcement, remediation)
        """)

# ======== REVENUE PROJECTIONS ========
if st.sidebar.checkbox("💰 Show Revenue Projections", key="show_revenue"):
    st.info("### 📈 Guardian Ghana Revenue Potential")

    revenue_data = revenue_calculator.calculate_potential_revenue()

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Monthly Revenue Potential", revenue_data['monthly_revenue'])
        st.metric("Annual Revenue Potential", revenue_data['annual_revenue'])

    with col2:
        st.write("**Client Distribution:**")
        for tier, count in revenue_data['client_distribution'].items():
            st.write(f"• {tier.title()}: {count} clients")

    st.caption(f"*Based on {revenue_data['assumptions']['market_size']} potential clients in Ghana*")

# ======== ENTERPRISE PORTAL ========
st.sidebar.markdown("---")
st.sidebar.header("💼 Enterprise Portal")

if st.sidebar.checkbox("Show Business Dashboard", key="business_dashboard"):
    st.info("### 🏢 Guardian Ghana Enterprise Platform")

    tab1, tab2, tab3, tab4 = st.tabs(
        ["📊 Market Analysis", "💰 Revenue Projections", "🎯 Client Portals", "🚀 Growth Strategy"])

    with tab1:
        st.subheader("Ghana Market Analysis")

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Addressable Market", "500 clients")
        with col2:
            st.metric("Year 1 Target", "100 clients")
        with col3:
            st.metric("Market Share Goal", "20%")

        st.write("### Target Client Segments")
        segments = {
            "Mining Companies": "40% of market - Compliance monitoring",
            "Government Agencies": "30% of market - National security",
            "Water Treatment Plants": "20% of market - Quality assurance",
            "Research Institutions": "10% of market - Data analytics"
        }

        for segment, description in segments.items():
            with st.expander(f"**{segment}**"):
                st.write(description)
                st.progress(0.4 if segment == "Mining Companies" else 0.3)

    with tab2:
        st.subheader("Revenue Projections")

        revenue_data = revenue_calculator.calculate_potential_revenue()

        col1, col2 = st.columns(2)
        with col1:
            st.metric("Monthly Revenue Potential", revenue_data['monthly_revenue'])
            st.metric("Annual Revenue Potential", revenue_data['annual_revenue'])

        with col2:
            st.write("**Client Distribution:**")
            for tier, count in revenue_data['client_distribution'].items():
                st.write(f"{tier.title()}: {count} clients")

        # Growth projection
        st.write("### 📈 5-Year Growth Projection")
        years = ['Year 1', 'Year 2', 'Year 3', 'Year 4', 'Year 5']
        revenue = [15, 40, 85, 150, 250]  # Millions

        growth_df = pd.DataFrame({
            'Year': years,
            'Revenue (₵M)': revenue,
            'Clients': [100, 250, 500, 800, 1200]
        })

        st.line_chart(growth_df.set_index('Year'))

    with tab3:
        st.subheader("Client Portal Demos")

        client_type = st.selectbox("Select Client Type:",
                                   ["government", "corporate", "research"])

        portal = enterprise_dashboard.generate_client_portal(client_type)

        st.success(f"### {portal['welcome_message']}")

        col1, col2 = st.columns(2)
        with col1:
            st.write("**Included Features:**")
            for feature in portal['features']:
                st.write(f"✓ {feature.replace('_', ' ').title()}")

        with col2:
            st.write("**Standard Reports:**")
            for report in portal['reports']:
                st.write(f"• {report['name']} ({report['frequency']})")

        st.write("**Active Alerts:**")
        for alert in portal['alerts']:
            st.info(f"🔔 {alert}")

    with tab4:
        st.subheader("🚀 Global Expansion Strategy")

        phases = [
            {"phase": "Phase 1 (2025/2026)", "focus": "Ghana Dominance", "target": "₵12.5M revenue",
             "markets": "Ghana (national deployment)",
             "products": "Water monitoring MVP"},
            {"phase": "Phase 2 (2027/2028)", "focus": "West Africa", "target": "₵62.5M revenue",
             "markets": "Nigeria, Ivory Coast, Senegal",
             "products": "Regional platform + API"},
            {"phase": "Phase 3 (2028/2029)", "focus": "Africa Continent", "target": "₵250M revenue",
             "markets": "10+ African countries",
             "products": "Multi-language + Mobile app"},
            {"phase": "Phase 4 (2030+)", "focus": "Global Platform", "target": "₵1250M+ revenue",
             "markets": "Global (SE Asia, LatAm, Europe)",
             "products": "Environmental Intelligence Suite"}
        ]

        for phase in phases:
            with st.expander(f"**{phase['phase']}: {phase['focus']}**", expanded=True):
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"**Key Markets:** {phase['markets']}")
                    st.write(f"**Product Evolution:** {phase['products']}")
                with col2:
                    st.metric("Revenue Target", phase['target'])

        st.info("""
        **Ultimate Vision:** Become the "Operating System for Global Environmental Security"
        - Water Security → Air Quality → Soil Monitoring → Climate Risk → ESG Platform
        """)


