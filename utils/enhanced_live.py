"""
Enhanced real-time system with true auto-refresh
"""
import streamlit as st
import pandas as pd
import random
from datetime import datetime, timedelta
import time
from data.sample_data import generate_sample_data, get_water_quality_status


class EnhancedLiveSystem:
    def __init__(self):
        self.refresh_interval = 20  # seconds
        self.update_cycle = 0
        self.last_update_time = None

        # River state tracking
        self.river_states = {}

    def start_live_mode(self):
        """Start enhanced live mode"""
        st.session_state.enhanced_live = True
        st.session_state.live_start_time = datetime.now()
        st.session_state.live_update_count = 0
        st.session_state.live_events = []

        # Initialize river states
        self._init_river_states()

        return True

    def stop_live_mode(self):
        """Stop live mode"""
        st.session_state.enhanced_live = False
        return True

    def _init_river_states(self):
        """Initialize tracking for each river"""
        rivers = ["Pra River", "Ankobra River", "Birim River", "Tano River", "Offin River"]
        for river in rivers:
            self.river_states[river] = {
                'status': 'normal',
                'last_event': None,
                'event_count': 0
            }

    def generate_live_data(self):
        """Generate realistic live data with trending patterns"""
        # Base data
        df = generate_sample_data(include_live_variation=False)

        # Add time-based trends
        current_hour = datetime.now().hour
        current_minute = datetime.now().minute

        # Mining activity patterns (more during day)
        if 6 <= current_hour <= 18:
            mining_factor = random.uniform(1.1, 1.4)
        else:
            mining_factor = random.uniform(0.8, 1.1)

        # Rainfall simulation (occasional events)
        rainfall_event = random.random() > 0.85  # 15% chance

        for idx, row in df.iterrows():
            river_name = row['river_name']

            # Get river state
            state = self.river_states.get(river_name, {'status': 'normal'})

            # Apply mining activity factor
            df.at[idx, 'turbidity_ntu'] = row['turbidity_ntu'] * mining_factor

            # Occasional pollution events based on risk level
            if row['risk_level'] == 'high' and random.random() > 0.9:
                # Simulate pollution spike
                df.at[idx, 'turbidity_ntu'] *= random.uniform(2, 4)
                df.at[idx, 'ph'] -= random.uniform(0.3, 1.0)

                # Record event
                self._record_event(river_name, 'pollution_spike')

            # Rainfall runoff effect
            if rainfall_event and random.random() > 0.5:
                df.at[idx, 'turbidity_ntu'] += random.randint(20, 60)
                self._record_event(river_name, 'rainfall_runoff')

            # Gradual trends (simulating ongoing mining)
            trend_factor = 1 + (self.update_cycle * 0.01)
            df.at[idx, 'turbidity_ntu'] *= trend_factor

            # Ensure values are within realistic bounds
            df.at[idx, 'turbidity_ntu'] = min(500, df.at[idx, 'turbidity_ntu'])
            df.at[idx, 'ph'] = max(4.0, min(9.0, df.at[idx, 'ph']))

        # Add status column
        df['status'] = df.apply(
            lambda row: get_water_quality_status(row['turbidity_ntu'], row['ph']),
            axis=1
        )

        # Update timestamp
        df['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        self.update_cycle += 1
        self.last_update_time = datetime.now()

        return df

    def _record_event(self, river_name, event_type):
        """Record a pollution event"""
        if river_name not in self.river_states:
            self.river_states[river_name] = {'status': 'normal', 'event_count': 0}

        self.river_states[river_name]['event_count'] += 1
        self.river_states[river_name]['last_event'] = {
            'type': event_type,
            'time': datetime.now().strftime("%H:%M:%S")
        }

        # Add to live events list
        event = {
            'time': datetime.now().strftime("%H:%M:%S"),
            'river': river_name,
            'type': event_type,
            'severity': 'warning' if event_type == 'rainfall_runoff' else 'alert'
        }

        if 'live_events' in st.session_state:
            st.session_state.live_events.append(event)
            # Keep only last 10 events
            if len(st.session_state.live_events) > 10:
                st.session_state.live_events = st.session_state.live_events[-10:]

    def get_live_status(self):
        """Get current live system status"""
        if not st.session_state.get('enhanced_live'):
            return {
                'active': False,
                'message': 'Live mode inactive'
            }

        # Calculate next refresh
        if self.last_update_time:
            elapsed = (datetime.now() - self.last_update_time).seconds
            next_refresh = max(0, self.refresh_interval - elapsed)
        else:
            next_refresh = self.refresh_interval

        # Get critical river count from latest data
        critical_count = 0
        if 'live_data_df' in st.session_state and st.session_state.live_data_df is not None:
            critical_count = len(st.session_state.live_data_df[
                                     st.session_state.live_data_df['status'] == "🔴 Critical"
                                     ])

        return {
            'active': True,
            'update_count': st.session_state.get('live_update_count', 0),
            'next_refresh_in': next_refresh,
            'critical_rivers': critical_count,
            'total_events': len(st.session_state.get('live_events', [])),
            'uptime': str(datetime.now() - st.session_state.get('live_start_time', datetime.now()))
        }

    def check_and_update(self):
        """Check if it's time to update and perform update"""
        if not st.session_state.get('enhanced_live'):
            return False

        # Check if enough time has passed
        if self.last_update_time:
            elapsed = (datetime.now() - self.last_update_time).seconds
            if elapsed < self.refresh_interval:
                return False

        # Perform update
        new_data = self.generate_live_data()
        st.session_state.live_data_df = new_data
        st.session_state.live_update_count = st.session_state.get('live_update_count', 0) + 1

        # Check for critical changes
        self._check_critical_changes(new_data)

        return True

    def _check_critical_changes(self, new_data):
        """Check for new critical rivers and trigger alerts"""
        if 'previous_critical_count' not in st.session_state:
            st.session_state.previous_critical_count = 0

        current_critical = len(new_data[new_data['status'] == "🔴 Critical"])
        previous_critical = st.session_state.previous_critical_count

        if current_critical > previous_critical:
            # New critical rivers detected
            new_critical = current_critical - previous_critical
            critical_rivers = new_data[new_data['status'] == "🔴 Critical"]['river_name'].tolist()

            # Store alert
            st.session_state.last_alert = {
                'type': 'critical',
                'count': new_critical,
                'rivers': critical_rivers[:3],  # First 3 rivers
                'time': datetime.now()
            }

        st.session_state.previous_critical_count = current_critical


# Create global instance
enhanced_live = EnhancedLiveSystem()