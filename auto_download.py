"""
Auto-Download Script — Guardian Ghana
Run this daily to download new NASA GPM data
"""

from utils.data_manager import data_manager
from datetime import datetime


def main():
    print("=" * 60)
    print("🚀 GUARDIAN GHANA - AUTO-DOWNLOAD")
    print("=" * 60)
    print(f"📅 Run: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    # Get latest data
    most_recent = data_manager.get_most_recent_local_date()
    if most_recent:
        print(f"📊 Most recent local data: {most_recent}")
    else:
        print("📊 No local data found")

    # Download missing
    print()
    data_manager.download_missing_data()

    # Show summary
    print()
    print("📊 Local data summary:")
    dates = data_manager.get_available_dates()
    if dates:
        print(f"   Total days with data: {len(dates)}")
        print(f"   Most recent: {max(dates)}")
        print(f"   Earliest: {min(dates)}")
    else:
        print("   No data available")

    print()
    print("=" * 60)
    print("🏁 AUTO-DOWNLOAD COMPLETE")


if __name__ == "__main__":
    main()