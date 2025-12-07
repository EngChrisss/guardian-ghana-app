import requests
import pandas as pd
import streamlit as st


def check_and_alert(df, predictions=None):
    """Check data for threshold breaches and send alerts - NOW WITH AI PREDICTIONS"""

    alerts_sent = 0

    # 1. Check CURRENT data alerts (existing functionality)
    critical_cases = df[df['status'] == "🔴 Critical"]

    for idx, row in critical_cases.iterrows():
        # Determine which parameter triggered the alert
        if row['turbidity_ntu'] > 100:
            alert_system.send_current_alert(
                row['river_name'],
                'Turbidity',
                row['turbidity_ntu'],
                100,
                row['status']
            )
            alerts_sent += 1
        elif row['ph'] < 5.5:
            alert_system.send_current_alert(
                row['river_name'],
                'pH',
                row['ph'],
                5.5,
                row['status']
            )
            alerts_sent += 1

    # 2. Check AI PREDICTION alerts (NEW FUNCTIONALITY)
    # AUTO-INCLUDE predictions if they exist in session state
    if predictions is None and 'predictions' in st.session_state:
        predictions = st.session_state.predictions

    if predictions:
        high_risk_predictions = [p for p in predictions if "CRITICAL" in p['risk_level'] or "HIGH" in p['risk_level']]

        st.info(f"🔍 Found {len(high_risk_predictions)} high-risk predictions to alert")

        for prediction in high_risk_predictions:
            success = alert_system.send_prediction_alert(prediction)
            if success:
                alerts_sent += 1
                st.success(f"✅ Sent prediction alert for {prediction['river_name']}")
            else:
                st.error(f"❌ Failed to send prediction alert for {prediction['river_name']}")

    return alerts_sent


class TelegramAlertSystem:
    def __init__(self):
        # THESE READ FROM YOUR secrets.toml FILE
        self.bot_token = st.secrets.get('TELEGRAM_BOT_TOKEN', 'YOUR_BOT_TOKEN')
        self.chat_id = st.secrets.get('TELEGRAM_CHAT_ID', 'YOUR_CHAT_ID')

    def send_current_alert(self, river_name, parameter, value, threshold, status):
        """Send alert for CURRENT water quality issues"""
        message = f"🚨 WATER QUALITY ALERT - CURRENT ISSUE\n"
        message += f"📍 River: {river_name}\n"
        message += f"📊 Parameter: {parameter}\n"
        message += f"📈 Value: {value} (Threshold: {threshold})\n"
        message += f"🔄 Status: {status}\n"
        message += f"⏰ Time: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        message += f"🔍 Action: Immediate investigation recommended"

        return self._send_telegram_message(message)

    def send_prediction_alert(self, prediction):
        """Send alert for AI-PREDICTED pollution risks"""
        try:
            message = f"🔮 AI PREDICTION ALERT - FUTURE RISK\n"
            message += f"📍 River: {prediction['river_name']}\n"
            message += f"🎯 Risk Level: {prediction['risk_level']}\n"
            message += f"📊 Risk Score: {prediction['risk_score']}/100\n"

            # Check if nearest_hotspot exists and has the expected structure
            if ('nearest_hotspot' in prediction and
                    prediction['nearest_hotspot'] and
                    'name' in prediction['nearest_hotspot']):

                message += f"📍 Nearest Hotspot: {prediction['nearest_hotspot']['name']}\n"
                message += f"📏 Distance: {prediction['nearest_hotspot'].get('distance_km', 'N/A')}km\n"
                message += f"🏭 Mining Type: {prediction['nearest_hotspot'].get('type', 'Unknown').replace('_', ' ').title()}\n"
            else:
                message += f"📍 Nearest Hotspot: Data not available\n"

            message += f"🔍 Key Factors:\n"

            if 'factors' in prediction and prediction['factors']:
                for factor in prediction['factors']:
                    message += f"   • {factor}\n"
            else:
                message += f"   • No specific factors identified\n"

            message += f"⏰ Prediction Time: {prediction.get('prediction_time', 'Unknown')}\n"
            message += f"🛡️ Action: Preventive monitoring recommended"

            return self._send_telegram_message(message)

        except Exception as e:
            print(f"Error creating prediction alert: {e}")
            # Fallback to simple alert
            simple_message = f"🔮 AI PREDICTION ALERT\nRiver: {prediction['river_name']}\nRisk: {prediction['risk_level']}\nScore: {prediction['risk_score']}"
            return self._send_telegram_message(simple_message)

    def send_system_alert(self, alert_type, details):
        """Send system-level alerts"""
        message = f"⚙️ SYSTEM ALERT - {alert_type}\n"
        message += f"📝 Details: {details}\n"
        message += f"⏰ Time: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}"

        return self._send_telegram_message(message)

    def _send_telegram_message(self, message):
        """Generic method to send Telegram messages"""
        url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
        payload = {
            'chat_id': self.chat_id,
            'text': message
        }

        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                print(f"✅ Telegram alert sent successfully: {message[:50]}...")
                return True
            else:
                print(f"❌ Telegram API error: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Telegram alert failed: {e}")
            return False

    # KEEP THIS FOR BACKWARD COMPATIBILITY (for your existing test alerts)
    def send_alert(self, river_name, parameter, value, threshold, status):
        """Legacy method for backward compatibility"""
        return self.send_current_alert(river_name, parameter, value, threshold, status)


# Initialize alert system
alert_system = TelegramAlertSystem()