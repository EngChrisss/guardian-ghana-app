"""
Auto-Download NASA GPM Rainfall Data
Downloads data for dates that are actually available
"""

import gpm
from datetime import datetime, timedelta
import os
import glob

def get_available_date_range():
    """
    Get the date range that NASA has available
    IMERG-FR has ~3-4 month latency
    """
    today = datetime.now().date()
    # IMERG-FR is available up to about 3-4 months ago
    # So we download from 4 months ago
    end_date = today - timedelta(days=120)  # 4 months ago
    start_date = end_date - timedelta(days=30)  # 30 days of data

    return start_date, end_date

def download_recent_rainfall():
    """Download available IMERG data"""
    start_date, end_date = get_available_date_range()

    print("=" * 60)
    print("🌧️ NASA GPM AUTO-DOWNLOAD")
    print("=" * 60)
    print(f"📡 Downloading IMERG-FR from {start_date} to {end_date}...")
    print(f"ℹ️  (IMERG-FR has ~3-4 month latency)")
    print()

    try:
        gpm.download(
            product="IMERG-FR",
            product_type="RS",
            version=7,
            start_time=datetime.combine(start_date, datetime.min.time()),
            end_time=datetime.combine(end_date, datetime.max.time()),
            storage="GES_DISC"
        )
        print()
        print("✅ Download complete!")
        print(f"📁 Data saved to: ./data/GPM/RS/V07/IMERG/IMERG-FR/")
        return True
    except Exception as e:
        print(f"❌ Download failed: {e}")
        return False

def check_data_availability():
    """Check what data is available locally"""
    print()
    print("📊 Checking local data availability...")
    print("-" * 40)

    available_dates = []

    # Check data from last 6 months
    for i in range(180):
        check_date = datetime.now().date() - timedelta(days=i)
        date_str = check_date.strftime("%Y/%m/%d")
        file_pattern = f"./data/GPM/RS/V07/IMERG/IMERG-FR/{date_str}/*.HDF5"
        files = glob.glob(file_pattern)

        if files:
            available_dates.append(check_date)

    if available_dates:
        print(f"✅ Found {len(available_dates)} days with data")
        print(f"   Most recent: {max(available_dates)}")
        print(f"   Earliest: {min(available_dates)}")

        # Show last 5 available dates
        print("\n   Recent available dates:")
        for date in sorted(available_dates, reverse=True)[:5]:
            date_str = date.strftime("%Y/%m/%d")
            file_pattern = f"./data/GPM/RS/V07/IMERG/IMERG-FR/{date_str}/*.HDF5"
            files = glob.glob(file_pattern)
            print(f"     ✅ {date}: {len(files)} files")
    else:
        print("❌ No data available locally")

    return available_dates

if __name__ == "__main__":
    print()
    print("🚀 STARTING AUTO-DOWNLOAD")
    print("=" * 60)

    # Check current data
    available = check_data_availability()

    # Check if we have data for the last 30 days
    if available:
        most_recent = max(available)
        today = datetime.now().date()
        days_behind = (today - most_recent).days

        if days_behind <= 30:
            print()
            print(f"✅ Data is recent! (Last available: {most_recent})")
            print(f"   You have all available data.")
        else:
            print()
            print(f"⚠️ Data is {days_behind} days behind.")
            print(f"   Most recent available date: {most_recent}")
            print(f"   Downloading available data...")
            download_recent_rainfall()
    else:
        print()
        print("📥 No data found. Downloading available data...")
        download_recent_rainfall()

    print()
    print("=" * 60)
    print("🏁 AUTO-DOWNLOAD COMPLETE")