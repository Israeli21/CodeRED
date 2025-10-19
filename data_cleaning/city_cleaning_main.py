import pandas as pd

# Read the CSV
df = pd.read_csv("../renewable_energies/cleaned_locations.csv")

# Define U.S. regions with states
regions = {
    "Northeast": [
        "Maine", "New Hampshire", "Vermont", "Massachusetts", "Rhode Island",
        "Connecticut", "New York", "New Jersey", "Pennsylvania"
    ],
    "Midwest": [
        "Ohio", "Michigan", "Indiana", "Wisconsin", "Illinois", "Minnesota",
        "Iowa", "Missouri", "North Dakota", "South Dakota", "Nebraska", "Kansas"
    ],
    "South": [
        "Delaware", "Maryland", "District of Columbia", "Virginia", "West Virginia",
        "North Carolina", "South Carolina", "Georgia", "Florida", "Kentucky",
        "Tennessee", "Mississippi", "Alabama", "Oklahoma", "Texas", "Arkansas", "Louisiana"
    ],
    "West": [
        "Idaho", "Montana", "Wyoming", "Nevada", "Utah", "Colorado", "Arizona",
        "New Mexico", "Alaska", "Washington", "Oregon", "California", "Hawaii"
    ]
}

# Function to assign region
def assign_region(state_name):
    if state_name == "District of Columbia":
        return "South (DC Outlier)"
    for region, states in regions.items():
        if state_name in states:
            return region
    return "Unknown"

# Apply region mapping
df["Region"] = df["state_name"].apply(assign_region)

# Optional: save the new CSV
df.to_csv("cleaned_locations_with_region.csv", index=False)

# Check
print(df.head(10))


