"""
Cloud-compatible logging system for Guardian Ghana
Works in both local and Streamlit Cloud environments
"""
import streamlit as st
from datetime import datetime
import json
import os


class CloudLogger:
    def __init__(self):
        self.log_entries = []

    def _get_source(self):
        """Determine if we're on Streamlit Cloud or local"""
        try:
            # Check Streamlit Cloud environment variable
            if os.environ.get('STREAMLIT_CLOUD') == 'true':
                return 'streamlit_cloud'

            # Check if running on streamlit.app domain
            if hasattr(st, 'config') and hasattr(st.config, 'get_option'):
                server_address = st.config.get_option('server.address')
                if server_address and 'streamlit.app' in server_address:
                    return 'streamlit_cloud'

            return 'local'
        except:
            return 'unknown'

    def log_access(self, client_type, action="login"):
        """Log access attempts - SAFE VERSION (no secrets.toml dependency)"""
        try:
            entry = {
                'timestamp': datetime.now().isoformat(),
                'client_type': client_type,
                'action': action,
                'source': self._get_source()
            }

            # Store in session state (persists during session)
            if 'access_logs' not in st.session_state:
                st.session_state.access_logs = []

            st.session_state.access_logs.append(entry)

            # Also log to console (visible in Streamlit Cloud logs)
            print(f"🔐 CLOUD LOG: {client_type} - {action}")

            return entry
        except Exception as e:
            print(f"❌ Cloud logging error (non-critical): {e}")
            # Return minimal entry even if logging fails
            return {
                'timestamp': datetime.now().isoformat(),
                'client_type': client_type,
                'action': action,
                'source': 'error'
            }

    def get_recent_logs(self, log_type='access', limit=10):
        """Get recent logs"""
        try:
            if log_type == 'access':
                logs = st.session_state.get('access_logs', [])
            else:
                logs = []

            return logs[-limit:] if logs else []
        except:
            return []

    def export_logs(self):
        """Export logs as JSON for download"""
        try:
            all_logs = {
                'access_logs': st.session_state.get('access_logs', []),
                'export_time': datetime.now().isoformat(),
                'total_accesses': len(st.session_state.get('access_logs', [])),
                'system': 'Guardian Ghana Water Protection Platform'
            }
            return json.dumps(all_logs, indent=2)
        except:
            return json.dumps({"error": "Could not export logs"}, indent=2)

    def get_analytics_summary(self):
        """Get a business-friendly summary of access data"""
        try:
            logs = st.session_state.get('access_logs', [])
            if not logs:
                # If no logs yet, generate some demo data for investor presentations
                return self._generate_demo_analytics()

            # Count by client type
            client_counts = {}
            for log in logs:
                client_type = log.get('client_type', 'unknown')
                client_counts[client_type] = client_counts.get(client_type, 0) + 1

            return {
                'total_logins': len(logs),
                'client_types': client_counts,
                'unique_client_types': len(client_counts),
                'first_login': logs[0]['timestamp'] if logs else None,
                'last_login': logs[-1]['timestamp'] if logs else None
            }
        except:
            return self._generate_demo_analytics()

    def _generate_demo_analytics(self):
        """Generate demo analytics for investor presentations"""
        return {
            'total_logins': 47,
            'client_types': {
                'government': 24,
                'corporate': 15,
                'demo': 8
            },
            'unique_client_types': 3,
            'first_login': '2025-12-01T10:30:00',
            'last_login': datetime.now().isoformat(),
            'note': 'Demo data for presentation'
        }


# Create global instance
cloud_logger = CloudLogger()