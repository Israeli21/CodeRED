# src/data_prep.py (Data Cleaning)
import pandas as pd

def load_solar_data(filepath="data/solar_data.csv"):
    """Load and clean solar data from Kaggle"""
    
    df = pd.read_csv(filepath)
    df = df.dropna()
    
    # Add location grouping if needed
    return df


def add_location_data(df):
    """Add location-based features"""
    
    # Aggregate data by location
    location_stats = df.groupby("location").agg({
        "irradiance": "mean",
        "temperature": "mean",
        "humidity": "mean",
        "power_output": "sum"
    }).reset_index()
    
    return location_stats
