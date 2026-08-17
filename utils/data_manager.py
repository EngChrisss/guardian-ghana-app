"""
Data Manager — Guardian Ghana
Handles NASA GPM data downloads and management
"""

import gpm
import glob
import os
from datetime import datetime, timedelta
import xarray as xr


class GPMDataManager:
    def __init__(self):
        self.base_path = "./data/GPM/RS/V07/IMERG/IMERG-FR/"
        self.product = "IMERG-FR"
        self.product_type = "RS"
        self.version = 7
        self.storage = "GES_DISC"

    def get_available_dates(self):
        """Get all dates that have data locally"""
        date_pattern = f"{self.base_path}*/"
        date_folders = glob.glob(date_pattern)

        available_dates = []
        for folder in date_folders:
            try:
                # Extract year/month from path
                parts = folder.split("/")
                if len(parts) >= 8:
                    year = int(parts[-3])
                    month = int(parts[-2])
                    day = 1  # We only store day 1 data
                    # Check if there are files
                    files = glob.glob(f"{folder}01/*.HDF5")
                    if files:
                        available_dates.append(datetime(year, month, 1).date())
            except:
                continue

        return sorted(available_dates)

    def get_most_recent_local_date(self):
        """Get the most recent date we have data for"""
        dates = self.get_available_dates()
        if dates:
            return max(dates)
        return None

    def get_most_recent_available_date(self):
        """
        Get the most recent date NASA has available.
        This attempts to find the latest date with data.
        """
        # Start from today and go backwards
        check_date = datetime.now().date()

        for _ in range(365):  # Check last 365 days
            try:
                # Check if we can access data for this date
                date_str = check_date.strftime("%Y/%m/%d")
                url = f"{self.base_path}{date_str}/"

                # Quick check - try to open a file
                test_files = glob.glob(f"{self.base_path}{date_str}/*.HDF5")
                if test_files:
                    return check_date

                # Try one more check with a small download attempt
                # If it fails, it's not available
                try:
                    gpm.download(
                        product=self.product,
                        product_type=self.product_type,
                        version=self.version,
                        start_time=datetime(check_date.year, check_date.month, check_date.day, 0, 0, 0),
                        end_time=datetime(check_date.year, check_date.month, check_date.day, 23, 59, 59),
                        storage=self.storage,
                        progress_bar=False
                    )
                    # If we get here, download worked
                    return check_date
                except:
                    pass

                check_date = check_date - timedelta(days=1)
            except:
                check_date = check_date - timedelta(days=1)

        return None

    def download_missing_data(self, start_date=None, end_date=None):
        """
        Download missing data for a date range
        """
        if start_date is None:
            # Check what we have
            current_data = self.get_available_dates()
            if current_data:
                start_date = max(current_data) + timedelta(days=1)
            else:
                # Use September 2025 as base
                start_date = datetime(2025, 9, 2).date()

        if end_date is None:
            end_date = datetime.now().date()

        print(f"📡 Checking for missing data from {start_date} to {end_date}")

        downloaded = 0
        current_date = start_date

        while current_date <= end_date:
            # Check if we already have this date
            date_str = current_date.strftime("%Y/%m/%d")
            existing_files = glob.glob(f"{self.base_path}{date_str}/*.HDF5")

            if not existing_files:
                print(f"   Downloading {current_date}...")
                try:
                    gpm.download(
                        product=self.product,
                        product_type=self.product_type,
                        version=self.version,
                        start_time=datetime(current_date.year, current_date.month, current_date.day, 0, 0, 0),
                        end_time=datetime(current_date.year, current_date.month, current_date.day, 23, 59, 59),
                        storage=self.storage
                    )
                    downloaded += 1
                except Exception as e:
                    print(f"   ❌ Failed: {e}")
            else:
                print(f"   ✅ Already have {current_date}")

            current_date += timedelta(days=1)

        print(f"✅ Download complete. Downloaded {downloaded} days.")
        return downloaded


# Create a global instance
data_manager = GPMDataManager()