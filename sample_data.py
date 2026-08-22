"""
Sample Data — Guardian Ghana
Generates sample water quality data for demonstration
"""

import pandas as pd
import random
from datetime import datetime


def generate_sample_data(include_live_variation=False):
    """Generate realistic sample water quality data for major Ghanaian rivers"""
    rivers = [
        {"name": "Pra River", "lat": 5.5, "lon": -1.0, "risk": "high"},
        {"name": "Ankobra River", "lat": 5.2, "lon": -2.2, "risk": "high"},
        {"name": "Birim River", "lat": 6.2, "lon": -1.1, "risk": "medium"},
        {"name": "Tano River", "lat": 6.3, "lon": -2.8, "risk": "medium"},
        {"name": "Offin River", "lat": 6.2, "lon": -1.9, "risk": "high"},
    ]

    data = []
    for river in rivers:
        base_turbidity = random.randint(50, 150) if river["risk"] == "high" else random.randint(10, 50)
        base_ph = random.uniform(5.0, 6.5) if river["risk"] == "high" else random.uniform(6.0, 7.5)

        if include_live_variation:
            time_variation = datetime.now().minute % 30
            base_turbidity += int(time_variation * 2)
            base_ph -= time_variation * 0.02

            if random.random() > 0.95:
                base_turbidity *= random.uniform(2, 4)
                base_ph -= random.uniform(0.5, 1.5)

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