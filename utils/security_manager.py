"""
Security Manager for Guardian Ghana
Manages access levels, permissions, and security features
"""
import streamlit as st
from datetime import datetime, timedelta
import hashlib


class SecurityManager:
    def __init__(self):
        self.access_levels = {
            'government_full': {
                'features': ['all_monitoring', 'epa_tools', 'enforcement', 'reports', 'export', 'alerts'],
                'restrictions': ['no_mining_portal'],
                'session_timeout': 7200  # 2 hours
            },
            'government_basic': {
                'features': ['basic_monitoring', 'public_reports', 'limited_export'],
                'restrictions': ['no_mining_portal', 'no_enforcement'],
                'session_timeout': 3600  # 1 hour
            },
            'mining_corporate': {
                'features': ['all_monitoring', 'mining_portal', 'compliance_tracking', 'epa_reports', 'cost_analysis'],
                'restrictions': ['no_government_tools'],
                'session_timeout': 14400  # 4 hours
            },
            'corporate_basic': {
                'features': ['basic_monitoring', 'limited_reports'],
                'restrictions': ['no_mining_portal', 'no_export'],
                'session_timeout': 3600  # 1 hour
            },
            'demo_limited': {
                'features': ['read_only_monitoring', 'demo_alerts'],
                'restrictions': ['no_export', 'no_reports', '7_day_limit'],
                'session_timeout': 1800  # 30 minutes
            }
        }

        # Password to access level mapping
        self.password_map = {
            'EPA2024': 'government_full',
            'WRC2024': 'government_basic',
            'MINING2024': 'mining_corporate',
            'CORPORATE2024': 'corporate_basic',
            'DEMO2024': 'demo_limited',
            'GUEST2024': 'demo_limited'
        }

    def validate_password(self, password):
        """Validate password and return access level"""
        if password in self.password_map:
            return self.password_map[password], True
        return None, False

    def get_features(self, access_level):
        """Get features for access level"""
        return self.access_levels.get(access_level, {}).get('features', [])

    def has_feature(self, access_level, feature):
        """Check if access level has specific feature"""
        return feature in self.get_features(access_level)

    def check_session_timeout(self, access_time):
        """Check if session has timed out"""
        if not access_time:
            return True

        access_level = st.session_state.get('access_level', 'demo_limited')
        timeout_seconds = self.access_levels.get(access_level, {}).get('session_timeout', 1800)

        elapsed = (datetime.now() - access_time).seconds
        return elapsed > timeout_seconds

    def hash_password(self, password):
        """Simple password hashing (in production use proper hashing)"""
        return hashlib.sha256(password.encode()).hexdigest()


# Create global instance
security_manager = SecurityManager()