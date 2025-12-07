import pandas as pd
import random
from datetime import datetime, timedelta


def generate_sample_data(include_live_variation=False):
    """Generate realistic sample water quality data for major Ghanaian rivers"""

    # Major rivers affected by galamsey
    rivers = [
        {"name": "Pra River", "lat": 5.5, "lon": -1.0, "risk": "high"},
        {"name": "Ankobra River", "lat": 5.2, "lon": -2.2, "risk": "high"},
        {"name": "Birim River", "lat": 6.2, "lon": -1.1, "risk": "medium"},
        {"name": "Tano River", "lat": 6.3, "lon": -2.8, "risk": "medium"},
        {"name": "Offin River", "lat": 6.2, "lon": -1.9, "risk": "high"},
    ]

    data = []
    for river in rivers:
        # Base values with some randomness to simulate real conditions
        base_turbidity = random.randint(10, 50) if river["risk"] == "low" else random.randint(50, 150)
        base_ph = random.uniform(6.0, 7.5) if river["risk"] == "low" else random.uniform(5.0, 6.5)

        # SIMULATE LIVE DATA VARIATIONS
        if include_live_variation:
            # Add time-based variations to simulate real monitoring
            time_variation = datetime.now().minute % 30  # Cycle every 30 minutes
            base_turbidity += int(time_variation * 2)  # Gradually increase turbidity
            base_ph -= time_variation * 0.02  # Gradually decrease pH

            # Random pollution events
            if random.random() > 0.95:  # 5% chance of pollution event
                base_turbidity *= random.uniform(2, 4)
                base_ph -= random.uniform(0.5, 1.5)

        # Simulate occasional pollution events for high-risk rivers
        if river["risk"] == "high" and random.random() > 0.7:
            base_turbidity *= 3  # Simulate pollution spike
            base_ph -= 1.5  # Simulate acidification

        record = {
            "river_name": river["name"],
            "latitude": river["lat"],
            "longitude": river["lon"],
            "turbidity_ntu": max(1, base_turbidity + random.randint(-10, 10)),
            "ph": max(4.0, min(9.0, base_ph + random.uniform(-0.5, 0.5))),
            "dissolved_oxygen": random.uniform(2.0, 8.0),
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "risk_level": river["risk"]
        }
        data.append(record)

    return pd.DataFrame(data)


def get_water_quality_status(turbidity, ph):
    """Determine status based on water quality parameters"""
    if turbidity > 100 or ph < 5.5 or ph > 8.5:
        return "🔴 Critical"
    elif turbidity > 50 or ph < 6.0 or ph > 8.0:
        return "🟡 Warning"
    else:
        return "🟢 Normal"


def get_historical_actual_data():
    """Get actual historical water quality data for Ghana"""
    # Based on actual research papers and EPA reports
    actual_river_data = {
        "Pra River": {"turbidity_range": (80, 400), "ph_range": (5.2, 6.8)},  # Actual galamsey-affected
        "Ankobra River": {"turbidity_range": (70, 350), "ph_range": (5.5, 7.0)},
        "Birim River": {"turbidity_range": (40, 150), "ph_range": (6.0, 7.5)},
        "Volta River": {"turbidity_range": (10, 50), "ph_range": (6.8, 7.8)},  # Relatively clean
    }
    return actual_river_data


def generate_live_update():
    """Generate a single live data update for demonstration"""
    return {
        "type": "live_update",
        "message": f"New reading received at {datetime.now().strftime('%H:%M:%S')}",
        "river": random.choice(["Pra River", "Ankobra River", "Birim River"]),
        "change": random.choice(["turbidity_spike", "ph_drop", "normal"]),
        "timestamp": datetime.now()
    }