
import json
import os
from datetime import datetime
from pathlib import Path
import sys
from dotenv import load_dotenv
import pandas as pd
import requests

sys.path.insert(0, str(Path().resolve().parent / "../src"))
from paths import *

load_dotenv()


# Lagos latitude and longitude
LATITUDE = 6.5244
LONGITUDE = 3.3792

API_KEY = os.getenv("OPEN_WEATHER_API_KEY") # open weather API key.



def extract_and_load_current_air_pollution_data():
    """
    Fetch current weather data from the OPENWEATHER API for the specified date.

    Returns:
        pd.DataFrame: A DataFrame containing the fetched data.
    """
    # API URL and parameters
    URL = "http://api.openweathermap.org/data/2.5/air_pollution"
    params = {
        "lat": LATITUDE,
        "lon": LONGITUDE,
        "appid": API_KEY
    }
    
    try:
        # Make GET request
        response = requests.get(URL, params=params)
        response.raise_for_status()  # Raise HTTPError for bad responses

        # Parse JSON response
        data = response.json()
        flatten_data = []
        
        if 'list' in data:
            for items in data["list"]:
                aqi = items["main"]["aqi"]
                co = items["components"]["co"]
                no = items["components"]["no"]
                no2 = items["components"]["no2"]
                o3 = items["components"]["o3"]
                so2 = items["components"]["so2"]
                pm2_5 = items["components"]["pm2_5"]
                pm10 = items["components"]["pm10"]
                nh3 = items["components"]["nh3"]
                timestamp = datetime.utcfromtimestamp(items["dt"]).strftime("%Y-%m-%d %H:%M:%S")
                
                flatten_data.append({
                    "aqi":aqi, "co":co, "no":no, "no2":no2, "o3":o3, "so2":so2, 
                    "pm2_5":pm2_5, "pm10":pm10, "nh3":nh3, "timestamp":timestamp
                })

            
            df = pd.DataFrame(flatten_data)
            # Convert timestamp column to datetime
            df["timestamp"] = pd.to_datetime(df["timestamp"])

            # Convert 'date' column to datetime format
            df['date'] = df["timestamp"].dt.date
            
            # Convert 'time' column to time format
            df['time'] = df["timestamp"].dt.time
            df['time'] = df['time'].astype(str)
            
            # create aqi_buket
            df["aqi_bucket"] = df["aqi"].apply(aqi_mapping_category)

            return df
    except Exception as err:
        print(f"Error fetching data")
        raise err


def extract_and_load_historical_air_pollution_data(start_date: str, end_date:str) -> str:
    """
    Fetch raw weather data from the OPENWEATHER API for the specified date.

    Parameters:
        start_date (int): start date of the data.
        end_date (int): end date of the data.

    Returns:
        pd.DataFrame: A DataFrame containing the fetched data.
    """
    
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    
    # API URL and parameters
    URL = "http://api.openweathermap.org/data/2.5/air_pollution/history"
    params = {
        "lat": LATITUDE,
        "lon": LONGITUDE,
        "start": int(start.timestamp()),
        "end": int(end.timestamp()),
        "appid": API_KEY
    }

    
    try:
        # Make GET request
        response = requests.get(URL, params=params)
        response.raise_for_status()  # Raise HTTPError for bad responses

        # Parse JSON response
        data = response.json()
        flatten_data = []
        
        
        if 'list' in data:
            for items in data["list"]:
                aqi = items["main"]["aqi"]
                co = items["components"]["co"]
                no = items["components"]["no"]
                no2 = items["components"]["no2"]
                o3 = items["components"]["o3"]
                so2 = items["components"]["so2"]
                pm2_5 = items["components"]["pm2_5"]
                pm10 = items["components"]["pm10"]
                nh3 = items["components"]["nh3"]
                timestamp = datetime.utcfromtimestamp(items["dt"]).strftime("%Y-%m-%d %H:%M:%S")
                
                flatten_data.append({
                    "aqi":aqi, "co":co, "no":no, "no2":no2, "o3":o3, "so2":so2, 
                    "pm2_5":pm2_5, "pm10":pm10, "nh3":nh3, "timestamp":timestamp
                })

            
            df = pd.DataFrame(flatten_data)
            
            if not Path(RAW_DATA_DIR).exists():
                    os.mkdir(RAW_DATA_DIR)
                    
            raw_file_name ="Air_Quality_20200101_to_20250201"
            file_path = RAW_DATA_DIR / f"{raw_file_name}.csv"
            
        
            df.to_csv(file_path)
            print(f"Data successfully fetched and saved to {file_path}")    
            
    except Exception as err:
        print(f"Error fetching data")
        raise err
    
    
def aqi_mapping_category(feature: int) -> str:
    """
    Maps an Air Quality Index (AQI) numeric value to its corresponding category.

    Parameters:
    feature (int): AQI value ranging from 1 to 5.

    Returns:
    str: Corresponding AQI category ("Good", "Fair", "Moderate", "Poor", "Very Poor") 
         or "Undefined" for invalid values.
    """
    categories = {
        1: "Good",
        2: "Fair",
        3: "Moderate",
        4: "Poor",
        5: "Very Poor"
    }
    return categories.get(feature, "Undefined")
    