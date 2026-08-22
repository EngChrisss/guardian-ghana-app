"""
Validation Data — Guardian Ghana
Historical pollution events for AI model validation
"""

HISTORICAL_EVENTS = [
    {
        "river": "Pra River",
        "date": "2019-03-15",
        "location": [5.65, -1.10],
        "type": "mercury_contamination",
        "severity": "high",
        "verified": True,
        "impact": "Major fish kill, water treatment plant shutdown"
    },
    {
        "river": "Ankobra River",
        "date": "2021-07-22",
        "location": [5.30, -2.35],
        "type": "fish_kill",
        "severity": "critical",
        "verified": True,
        "impact": "Large-scale aquatic life destruction"
    },
    {
        "river": "Birim River",
        "date": "2018-11-10",
        "location": [6.25, -1.15],
        "type": "diamond_mining_waste",
        "severity": "medium",
        "verified": True,
        "impact": "Water discoloration, community complaints"
    },
]


def calculate_distance(loc1, loc2):
    """Calculate distance between two coordinates"""
    return ((loc1[0] - loc2[0]) ** 2 + (loc1[1] - loc2[1]) ** 2) ** 0.5


def validate_predictions(predictions):
    """Validate AI predictions against historical events"""
    if not predictions:
        return {"accuracy": "0%", "precision": "0%", "recall": "0%", "tested_events": 0}

    matches = 0
    true_positives = 0
    false_positives = 0
    false_negatives = 0

    for event in HISTORICAL_EVENTS:
        event_matched = False
        for prediction in predictions:
            distance = calculate_distance(
                event['location'],
                [prediction['latitude'], prediction['longitude']]
            )
            if distance < 0.8 and prediction['risk_score'] > 50:
                event_matched = True
                true_positives += 1
                break

        if event_matched:
            matches += 1
        else:
            false_negatives += 1

    for prediction in predictions:
        if prediction['risk_score'] > 50:
            has_nearby_event = False
            for event in HISTORICAL_EVENTS:
                distance = calculate_distance(
                    event['location'],
                    [prediction['latitude'], prediction['longitude']]
                )
                if distance < 0.8:
                    has_nearby_event = True
                    break
            if not has_nearby_event:
                false_positives += 1

    total_events = len(HISTORICAL_EVENTS)
    accuracy = (matches / total_events) * 100 if total_events > 0 else 0
    precision = (true_positives / (true_positives + false_positives)) * 100 if (true_positives + false_positives) > 0 else 0
    recall = (true_positives / (true_positives + false_negatives)) * 100 if (true_positives + false_negatives) > 0 else 0

    return {
        'accuracy': f"{accuracy:.1f}%",
        'precision': f"{precision:.1f}%",
        'recall': f"{recall:.1f}%",
        'tested_events': total_events,
        'matched_events': matches
    }