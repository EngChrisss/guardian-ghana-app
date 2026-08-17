"""
Rainfall Service — Guardian Ghana
Provides real-time rainfall data from NASA GPM
"""

import glob
from datetime import datetime, timedelta

# ============================================
# SAFE IMPORTS FOR CLOUD DEPLOYMENT
# ============================================
try:
    import xarray as xr
    import netCDF4
    HAS_DATA_LIBS = True
    print("✅ xarray/netCDF4 loaded successfully")
except ImportError:
    HAS_DATA_LIBS = False
    print("⚠️ xarray/netCDF4 not available - using pre-downloaded data")
# ============================================

# Constants
ANKOBRA_LAT_MIN = 5.0
ANKOBRA_LAT_MAX = 5.8
ANKOBRA_LON_MIN = -2.5
ANKOBRA_LON_MAX = -1.8

DATA_DIR = "./data/GPM/RS/V07/IMERG/IMERG-FR/"


def get_ankobra_rainfall(date):
    """
    Get rainfall data for Ankobra Basin for a given date.
    Returns None if xarray is not available or no data found.
    """
    # If xarray isn't available, return None
    if not HAS_DATA_LIBS:
        print("⚠️ xarray not available - cannot read data")
        return None
    
    date_str = date.strftime("%Y/%m/%d")
    file_pattern = f"{DATA_DIR}{date_str}/*.HDF5"
    files = sorted(glob.glob(file_pattern))
    
    if not files:
        return None
    
    results = []
    
    for file in files:
        try:
            ds = xr.open_dataset(file, group='Grid')
            
            ankobra = ds.sel(
                lat=slice(ANKOBRA_LAT_MIN, ANKOBRA_LAT_MAX),
                lon=slice(ANKOBRA_LON_MIN, ANKOBRA_LON_MAX)
            )
            
            rain = ankobra['precipitation']
            avg_rain = float(rain.mean().values)
            
            time_val = ds.time.values[0]
            
            results.append({
                'time': time_val,
                'avg_rainfall': avg_rain,
                'max_rainfall': float(rain.max().values)
            })
            
            ds.close()
            
        except Exception as e:
            print(f"Error with {file}: {e}")
            continue
    
    if not results:
        return None
    
    # Calculate totals
    total_rain = sum(r['avg_rainfall'] for r in results)
    avg_rain_hour = total_rain / len(results)
    max_rain_hour = max(r['max_rainfall'] for r in results)
    
    return {
        'date': date,
        'hourly_data': results,
        'total_mm': total_rain,
        'avg_mm_per_hr': avg_rain_hour,
        'max_mm_per_hr': max_rain_hour,
        'hours_with_rain': sum(1 for r in results if r['avg_rainfall'] > 0)
    }


def get_live_rainfall():
    """
    Get rainfall data with fallback to demo data
    """
    # Step 1: Try today's data
    today = datetime.now().date()
    data = get_ankobra_rainfall(today)
    
    if data:
        return {
            'status': 'live',
            'data': data,
            'message': f"Live NASA GPM data for {today}"
        }
    
    # Step 2: Try yesterday
    yesterday = today - timedelta(days=1)
    data = get_ankobra_rainfall(yesterday)
    
    if data:
        return {
            'status': 'delayed',
            'data': data,
            'message': f"Most recent: {yesterday} (NASA GPM processing delay)"
        }
    
    # Step 3: Fallback to known good data (September 2025)
    fallback_date = datetime(2025, 9, 1).date()
    data = get_ankobra_rainfall(fallback_date)
    
    if data:
        return {
            'status': 'historical',
            'data': data,
            'message': f"Historical data: {fallback_date} (NASA GPM)"
        }
    
    # Step 4: Nothing available
    return {
        'status': 'unavailable',
        'data': None,
        'message': "No NASA GPM data available"
    }


def get_rainfall_status():
    """Simple status check for Guardian Ghana dashboard."""
    live = get_live_rainfall()
    
    if live['status'] == 'live':
        return f"{live['data']['total_mm']:.1f} mm ✅ Live"
    elif live['status'] == 'delayed':
        return f"{live['data']['total_mm']:.1f} mm ⏳ Delayed"
    elif live['status'] == 'historical':
        return f"{live['data']['total_mm']:.1f} mm 📊 NASA"
    else:
        return "⚠️ No data"


if __name__ == "__main__":
    # Test the module
    print("Testing rainfall_service.py")
    print("-" * 40)
    
    live = get_live_rainfall()
    print(f"Status: {live['status']}")
    print(f"Message: {live['message']}")
    
    if live['data']:
        print(f"Total rainfall: {live['data']['total_mm']:.2f} mm")
