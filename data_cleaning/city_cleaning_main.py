import pandas as pd

df = pd.read_csv("../renewable_energies/uscities.csv")

# Select only the columns you need
clean_df = df[["city","state_name", "lat", "lng"]]

# Take the first 100 rows
clean_df = clean_df.head(100)

# Save to a new CSV file
clean_df.to_csv("cleaned_locations.csv", index=False)


