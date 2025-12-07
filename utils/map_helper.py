import folium
import streamlit as st
import pandas as pd


# ======== GEOFENCING FUNCTIONS ========
def create_protected_zones():
    """Define protected zones (geofences) for critical water bodies"""
    protected_zones = [
        {
            "name": "Pra River Protected Zone",
            "coordinates": [[5.8, -1.3], [5.8, -0.8], [5.3, -0.8], [5.3, -1.3]],
            "color": "red",
            "fill_opacity": 0.1
        },
        {
            "name": "Ankobra Critical Area",
            "coordinates": [[5.4, -2.4], [5.4, -2.0], [5.0, -2.0], [5.0, -2.4]],
            "color": "orange",
            "fill_opacity": 0.1
        }
    ]
    return protected_zones


def add_geofences_to_map(ghana_map):
    """Add protected zone polygons to the map"""
    protected_zones = create_protected_zones()

    for zone in protected_zones:
        folium.Polygon(
            locations=zone["coordinates"],
            popup=zone["name"],
            tooltip=zone["name"],
            color=zone["color"],
            fill=True,
            fill_color=zone["color"],
            fill_opacity=zone["fill_opacity"]
        ).add_to(ghana_map)

    return ghana_map


# ======== PREDICTION FUNCTIONS ========
def add_predictions_to_map(ghana_map, predictions):
    """Add prediction markers to the map"""
    if not predictions:
        return ghana_map

    for pred in predictions:
        # Determine marker color based on risk
        if "HIGH" in pred['risk_level']:
            color = 'red'
        elif "MEDIUM" in pred['risk_level']:
            color = 'orange'
        else:
            color = 'green'

        # Create prediction popup
        popup_text = f"""
        <b>🚨 PREDICTION: {pred['river_name']}</b><br>
        <b>Risk Level:</b> {pred['risk_level']}<br>
        <b>Confidence:</b> {pred['confidence']}%<br>
        <b>Timeframe:</b> {pred['timeframe']}<br>
        <b>Reasons:</b> {', '.join(pred['reasons'])}<br>
        <b>Generated:</b> {pred['prediction_time']}<br>
        <i>AI-powered risk assessment</i>
        """

        # Add prediction marker (different icon to distinguish from current data)
        folium.Marker(
            location=[pred['latitude'], pred['longitude']],
            popup=folium.Popup(popup_text, max_width=300),
            icon=folium.Icon(color=color, icon='exclamation-triangle', prefix='fa'),
            tooltip=f"PREDICTION: {pred['river_name']} - {pred['risk_level']}"
        ).add_to(ghana_map)

    return ghana_map


def create_ghana_water_map(df, predictions=None):
    """Create a Folium map with water quality monitoring points and predictions"""

    # Center map on Ghana
    ghana_map = folium.Map(location=[7.9465, -1.0232], zoom_start=7)

    # Add geofences first
    ghana_map = add_geofences_to_map(ghana_map)

    # Add PREDICTIONS second (so they appear under current data)
    if predictions:
        ghana_map = add_predictions_to_map(ghana_map, predictions)

    # Add CURRENT DATA markers last (on top)
    for idx, row in df.iterrows():
        # Determine color based on status
        if row['turbidity_ntu'] > 100 or row['ph'] < 5.5:
            color = 'red'
        elif row['turbidity_ntu'] > 50 or row['ph'] < 6.0:
            color = 'orange'
        else:
            color = 'green'

        # Create popup text
        popup_text = f"""
        <b>{row['river_name']}</b><br>
        Status: {row.get('status', 'Unknown')}<br>
        Turbidity: {row['turbidity_ntu']} NTU<br>
        pH: {row['ph']:.2f}<br>
        DO: {row['dissolved_oxygen']:.2f} mg/L<br>
        Last Update: {row['timestamp']}
        """

        # Add marker to map
        folium.Marker(
            location=[row['latitude'], row['longitude']],
            popup=folium.Popup(popup_text, max_width=300),
            icon=folium.Icon(color=color, icon='tint', prefix='fa'),
            tooltip=f"Click for {row['river_name']} details"
        ).add_to(ghana_map)

    return ghana_map


def create_risk_overlay_map(df, risk_data=None):
    """FIXED: Create map with proper error handling and data validation"""

    # Center map on Ghana with better default view
    ghana_map = folium.Map(
        location=[7.9465, -1.0232],
        zoom_start=7,
        tiles='OpenStreetMap'  # Ensure tiles load properly
    )

    # Add risk heatmap if we have valid prediction data
    if risk_data is not None and not risk_data.empty:
        st.info(f"🔄 Rendering {len(risk_data)} risk points...")

        # Validate required columns exist
        required_columns = ['lat', 'lon', 'risk_score', 'risk_level', 'river_name']
        missing_columns = [col for col in required_columns if col not in risk_data.columns]

        if missing_columns:
            st.error(f"❌ Missing columns in risk data: {missing_columns}")
            # Fallback to current monitoring map
            return create_ghana_water_map(df)

        # Add risk points to map with CORRECT colors
        valid_points = 0
        for idx, row in risk_data.iterrows():
            try:
                # Validate coordinates
                if (pd.isna(row['lat']) or pd.isna(row['lon']) or
                        row['lat'] < 4.0 or row['lat'] > 12.0 or
                        row['lon'] < -4.0 or row['lon'] > 2.0):
                    continue  # Skip invalid coordinates

                # DETERMINE CORRECT COLOR BASED ON RISK LEVEL
                risk_score = float(row['risk_score']) if pd.notna(row['risk_score']) else 0
                risk_level = str(row['risk_level'])

                if "CRITICAL" in risk_level or risk_score >= 80:
                    color = 'red'
                    risk_text = "🔴 CRITICAL"
                elif "HIGH" in risk_level or risk_score >= 60:
                    color = 'orange'
                    risk_text = "🟠 HIGH"
                elif "MEDIUM" in risk_level or risk_score >= 40:
                    color = 'yellow'
                    risk_text = "🟡 MEDIUM"
                else:
                    color = 'green'
                    risk_text = "🟢 LOW"

                # Create popup content
                popup_content = f"""
                <b>AI PREDICTION: {row['river_name']}</b><br>
                <b>Risk Level:</b> {risk_text}<br>
                <b>Risk Score:</b> {risk_score:.0f}/100<br>
                <b>Nearest Hotspot:</b> {row.get('nearest_hotspot', 'Unknown')}<br>
                <i>AI-powered pollution risk forecast</i>
                """

                # Add risk prediction marker
                folium.CircleMarker(
                    location=[row['lat'], row['lon']],
                    radius=8 + (risk_score / 20),  # Size based on risk
                    popup=folium.Popup(popup_content, max_width=300),
                    tooltip=f"PREDICTION: {risk_text} - {row['river_name']}",
                    color=color,
                    fillColor=color,
                    fill=True,
                    fillOpacity=0.7,
                    weight=1
                ).add_to(ghana_map)

                valid_points += 1

            except Exception as e:
                # Skip this point but continue with others
                continue

        st.success(f"✅ Successfully rendered {valid_points} risk points")

        if valid_points == 0:
            st.warning("⚠️ No valid risk points to display - showing current monitoring instead")
            return create_ghana_water_map(df)

    # Add current monitoring data (on top)
    for idx, row in df.iterrows():
        try:
            # Determine color based on current status
            if row['turbidity_ntu'] > 100 or row['ph'] < 5.5:
                color = 'red'
                status_text = "🔴 CRITICAL"
            elif row['turbidity_ntu'] > 50 or row['ph'] < 6.0:
                color = 'orange'
                status_text = "🟡 WARNING"
            else:
                color = 'green'
                status_text = "🟢 NORMAL"

            popup_text = f"""
            <b>CURRENT: {row['river_name']}</b><br>
            <b>Status:</b> {status_text}<br>
            <b>Turbidity:</b> {row['turbidity_ntu']} NTU<br>
            <b>pH:</b> {row['ph']:.2f}<br>
            <b>Last Update:</b> {row['timestamp']}
            """

            folium.Marker(
                location=[row['latitude'], row['longitude']],
                popup=folium.Popup(popup_text, max_width=300),
                icon=folium.Icon(color=color, icon='tint', prefix='fa'),
                tooltip=f"CURRENT: {row['river_name']} - {status_text}"
            ).add_to(ghana_map)

        except Exception as e:
            continue

    return ghana_map

def display_map(folium_map):
    """Display Folium map in Streamlit without streamlit-folium"""
    import tempfile
    import os

    # Save the map to a temporary HTML file
    with tempfile.NamedTemporaryFile(delete=False, suffix='.html') as tmp:
        folium_map.save(tmp.name)

        # Read the HTML file and display it
        with open(tmp.name, 'r', encoding='utf-8') as f:
            html_content = f.read()

        st.components.v1.html(html_content, height=500)

    # Clean up the temporary file
    os.unlink(tmp.name)