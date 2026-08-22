"""
Rainfall Chart Module — Guardian Ghana
Displays rainfall trends from NASA GPM data
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
from rainfall_service import get_ankobra_rainfall


def display_rainfall_chart():
    """Display rainfall chart for the Ankobra Basin"""

    # Use September 2025 data
    date = datetime(2025, 9, 1).date()
    rain_data = get_ankobra_rainfall(date)

    if not rain_data:
        st.warning("No rainfall data available")
        return

    # Convert hourly data to DataFrame
    df = pd.DataFrame(rain_data['hourly_data'])

    # Extract time as string for better display
    df['time_str'] = df['time'].apply(lambda x: str(x)[11:16])

    # Create the chart
    fig = px.bar(
        df,
        x='time_str',
        y='avg_rainfall',
        title=f"Rainfall on {date.strftime('%B %d, %Y')} — Ankobra Basin",
        labels={
            'time_str': 'Time (UTC)',
            'avg_rainfall': 'Rainfall (mm/hr)'
        },
        color='avg_rainfall',
        color_continuous_scale='Blues',
        height=400
    )

    # Add a line for average
    avg_rain = df['avg_rainfall'].mean()
    fig.add_hline(
        y=avg_rain,
        line_dash="dash",
        line_color="red",
        annotation_text=f"Avg: {avg_rain:.2f} mm/hr"
    )

    # Update layout
    fig.update_layout(
        xaxis_tickangle=-45,
        showlegend=False,
        margin=dict(l=40, r=40, t=60, b=80)
    )

    # Display
    st.plotly_chart(fig, use_container_width=True)

    # Show stats
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Rainfall", f"{rain_data['total_mm']:.1f} mm")
    with col2:
        st.metric("Max Hourly Rate", f"{rain_data['max_mm_per_hr']:.2f} mm/hr")
    with col3:
        st.metric("Hours with Rain", f"{rain_data['hours_with_rain']}/24")


def display_rainfall_summary():
    """Display a compact rainfall summary for the dashboard"""

    date = datetime(2025, 9, 1).date()
    rain_data = get_ankobra_rainfall(date)

    if not rain_data:
        st.info("No rainfall data available")
        return

    # Summary cards
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("📅 Date", date.strftime("%b %d, %Y"))
    with col2:
        st.metric("🌧️ Total", f"{rain_data['total_mm']:.1f} mm")
    with col3:
        st.metric("⏱️ Max", f"{rain_data['max_mm_per_hr']:.2f} mm/hr")
    with col4:
        st.metric("🕐 Rain Hours", f"{rain_data['hours_with_rain']}/24")


if __name__ == "__main__":
    # Test the module
    display_rainfall_chart()