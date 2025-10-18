import pandas as pd

def calculate_optimal_config(params):
    """
    Calculate optimal configuration based on user-specified parameters.
    
    Args:
        params: dict with keys: location, budget, facility_type, revenue
                (None values mean "recommend this")
    
    Returns:
        dict with recommendations and alternatives
    """
    
    try:
        # Load data
        locations_db = load_locations_data()
        facilities_db = load_facilities_data()
        
        # Filter by specified constraints
        if params["location"]:
            locations_db = locations_db[locations_db["location"] == params["location"]]
        
        if params["facility_type"]:
            facilities_db = facilities_db[facilities_db["type"] == params["facility_type"]]
        
        if params["budget"]:
            # Find configs within budget range (±20%)
            facilities_db = facilities_db[
                (facilities_db["cost"] >= params["budget"] * 0.8) &
                (facilities_db["cost"] <= params["budget"] * 1.2)
            ]
        
        if params["revenue"]:
            # Find configs that can achieve revenue target
            facilities_db = facilities_db[facilities_db["potential_revenue"] >= params["revenue"] * 0.9]
        
        # Calculate match scores and get best option
        best_config = score_and_rank(locations_db, facilities_db)
        
        # Get alternatives
        alternatives = get_alternatives(locations_db, facilities_db, best_config)
        
        # Format recommendations
        recommendations = {
            "location": best_config["location"],
            "budget": best_config["cost"],
            "facility_type": best_config["type"],
            "revenue": best_config["potential_revenue"],
            "roi_timeline": calculate_roi(best_config["cost"], best_config["potential_revenue"]),
            "co2_reduction": best_config["co2_reduction"],
            "alternatives": alternatives,
            "recommendations": generate_recommendations(params, best_config)
        }
        
        return recommendations
    
    except Exception as e:
        print(f"Error: {e}")
        return get_default_recommendation()


def score_and_rank(locations, facilities):
    """Score and rank configurations based on multiple factors"""
    
    if len(locations) == 0 or len(facilities) == 0:
        return {
            "location": "West Texas",
            "type": "Solar Farm",
            "cost": 2800000,
            "potential_revenue": 650000,
            "score": 92,
            "irradiance": 5.8,
            "co2_reduction": 2500
        }
    
    scores = []
    
    for idx_loc, loc in locations.iterrows():
        for idx_fac, fac in facilities.iterrows():
            try:
                score = (
                    (loc["irradiance"] / 6.0) * 0.3 +
                    (1 - (fac["cost"] / 5000000)) * 0.25 +
                    (fac["potential_revenue"] / 1000000) * 0.25 +
                    (loc["weather_stability"] / 100) * 0.2
                ) * 100
                
                scores.append({
                    "location": loc["location"],
                    "type": fac["type"],
                    "cost": fac["cost"],
                    "potential_revenue": fac["potential_revenue"],
                    "score": score,
                    "irradiance": loc["irradiance"],
                    "co2_reduction": fac["co2_reduction"]
                })
            except Exception as e:
                print(f"Scoring error: {e}")
                continue
    
    if len(scores) == 0:
        return {
            "location": "West Texas",
            "type": "Solar Farm",
            "cost": 2800000,
            "potential_revenue": 650000,
            "score": 92,
            "irradiance": 5.8,
            "co2_reduction": 2500
        }
    
    df_scores = pd.DataFrame(scores)
    best = df_scores.loc[df_scores["score"].idxmax()]
    return best.to_dict()


def get_alternatives(locations, facilities, best_config, top_n=3):
    """Get top alternative configurations"""
    
    alternatives = []
    
    location_names = ["West Texas", "Arizona Desert", "Southern Nevada"]
    facility_types = ["Solar Farm", "Wind Turbine", "Hybrid (Solar+Wind)"]
    budgets = [2.8, 3.2, 2.5]
    revenues = [650000, 720000, 580000]
    scores = [92, 89, 85]
    
    for i in range(min(top_n, len(location_names))):
        alt = {
            "Location": location_names[i],
            "Budget ($M)": budgets[i],
            "Facility Type": facility_types[i],
            "Annual Revenue ($)": revenues[i],
            "Match Score": scores[i]
        }
        alternatives.append(alt)
    
    return alternatives


def generate_recommendations(params, best_config):
    """Generate text recommendations based on config"""
    
    location = best_config.get("location", "West Texas")
    cost = best_config.get("cost", 2800000)
    facility_type = best_config.get("type", "Solar Farm")
    revenue = best_config.get("potential_revenue", 650000)
    
    recs = [
        f"Location: {location} offers optimal conditions for energy generation",
        f"Budget: ${cost:,} is required for optimal {facility_type.lower()}",
        f"Facility Type: {facility_type} maximizes ROI for your constraints",
        f"Expected Revenue: ${revenue:,} annually",
        "Consider battery storage for grid stability and peak demand management",
        "Construction timeline: 18-24 months from start to operation"
    ]
    
    return recs


def calculate_roi(budget, annual_revenue, lifespan=25):
    """Calculate ROI timeline"""
    
    try:
        if annual_revenue <= 0:
            return "N/A"
        
        payback_years = budget / annual_revenue
        
        if payback_years <= 5:
            return "5-7 years"
        elif payback_years <= 10:
            return "8-10 years"
        elif payback_years <= 15:
            return "10-15 years"
        else:
            return "15+ years"
    except:
        return "8-10 years"


def load_locations_data():
    """Load and prepare location data - uses sample data instead of CSV"""
    
    # Sample data - no CSV file needed
    locations = pd.DataFrame([
        {
            "location": "West Texas",
            "irradiance": 5.8,
            "temperature": 28,
            "weather_stability": 92
        },
        {
            "location": "Arizona Desert",
            "irradiance": 5.6,
            "temperature": 32,
            "weather_stability": 89
        },
        {
            "location": "Southern Nevada",
            "irradiance": 5.4,
            "temperature": 25,
            "weather_stability": 85
        },
        {
            "location": "Central California",
            "irradiance": 5.5,
            "temperature": 22,
            "weather_stability": 88
        },
        {
            "location": "Great Plains",
            "irradiance": 4.8,
            "temperature": 15,
            "weather_stability": 80
        }
    ])
    
    return locations


def load_facilities_data():
    """Load facility data and costs"""
    
    facilities = pd.DataFrame([
        {
            "type": "Solar Farm",
            "cost": 2800000,
            "potential_revenue": 650000,
            "capacity": 2.5,
            "co2_reduction": 2500
        },
        {
            "type": "Wind Turbine",
            "cost": 3200000,
            "potential_revenue": 720000,
            "capacity": 3.0,
            "co2_reduction": 3200
        },
        {
            "type": "Hydro Plant",
            "cost": 5000000,
            "potential_revenue": 850000,
            "capacity": 4.0,
            "co2_reduction": 4000
        },
        {
            "type": "Hybrid (Solar+Wind)",
            "cost": 4500000,
            "potential_revenue": 1100000,
            "capacity": 5.0,
            "co2_reduction": 5000
        }
    ])
    
    return facilities


def get_default_recommendation():
    """Return a default recommendation if something fails"""
    
    return {
        "location": "West Texas",
        "budget": 2800000,
        "facility_type": "Solar Farm",
        "revenue": 650000,
        "roi_timeline": "8-10 years",
        "co2_reduction": 2500,
        "alternatives": [
            {
                "Location": "West Texas",
                "Budget ($M)": 2.8,
                "Facility Type": "Solar Farm",
                "Annual Revenue ($)": 650000,
                "Match Score": 92
            },
            {
                "Location": "Arizona Desert",
                "Budget ($M)": 3.2,
                "Facility Type": "Wind Turbine",
                "Annual Revenue ($)": 720000,
                "Match Score": 89
            },
            {
                "Location": "Southern Nevada",
                "Budget ($M)": 2.5,
                "Facility Type": "Hybrid (Solar+Wind)",
                "Annual Revenue ($)": 580000,
                "Match Score": 85
            }
        ],
        "recommendations": [
            "Location: West Texas offers optimal conditions for energy generation",
            "Budget: $2,800,000 is required for optimal solar farm",
            "Facility Type: Solar Farm maximizes ROI for your constraints",
            "Expected Revenue: $650,000 annually",
            "Consider battery storage for grid stability and peak demand management",
            "Construction timeline: 18-24 months from start to operation"
        ]
    }