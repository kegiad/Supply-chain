import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
# Base data for districts (2015 data)
data_2015 = {
    "District": [
        "Thiruvananthapuram", "Kollam", "Pathanamthitta", "Alappuzha",
        "Kottayam", "Idukki", "Ernakulam", "Thrissur", "Palakkad",
        "Malappuram", "Kozhikode", "Wayanad", "Kannur", "Kasaragode"
    ],
    "Area (Ha)": [2293, 3330, 1707, 616, 3215, 42694, 1867, 1790, 2510, 2938, 3474, 12498, 4269, 2747],
    "Production (Tonnes)": [972, 1093, 599, 134, 1150, 25495, 527, 479, 954, 460, 934, 6593, 1553, 1189]
}

# Create a base DataFrame for 2015
df_2015 = pd.DataFrame(data_2015)

# Calculate yield for 2015 (Tonnes per Hectare)
df_2015["Yield (Tonnes/Ha)"] = df_2015["Production (Tonnes)"] / df_2015["Area (Ha)"]

# Generate data for 2000 to 2020
years = list(range(2001, 2021))
synthetic_data = []

np.random.seed(42)
for year in years:
    year_data = df_2015.copy()
    year_data["Year"] = year

    # Introduce small random changes to the area (±5%)
    area_change = np.random.uniform(0.95, 1.05, size=len(year_data))  # Random change factor
    year_data["Area (Ha)"] = (year_data["Area (Ha)"] * area_change).round(2)

    # Calculate production based on new area and 2015 yield
    year_data["Production (Tonnes)"] = (year_data["Area (Ha)"] * year_data["Yield (Tonnes/Ha)"]).round(2)

    # Drop the yield column if not needed in the final dataset
    year_data = year_data.drop(columns=["Yield (Tonnes/Ha)"])

    # Append to the synthetic data list
    synthetic_data.append(year_data)

# Combine all years into a single DataFrame
final_df = pd.concat(synthetic_data, ignore_index=True)

# Display the first few rows of the final dataset
print(final_df)

