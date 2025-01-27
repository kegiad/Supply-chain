import pandas as pd

# Load the original CSV file
file_path = 'pepper_data_2001_2020.csv'  # Replace with your file path
df = pd.read_csv(file_path)

# Add columns for Natural Disaster and Severity
# Initialize all values to 0 (no disaster)
df['Disruption'] = 0
df['Severity (%)'] = 0

# Define years with natural disasters and their severity
disaster_years = {2018: 31, 2019: 28}

# Add natural disaster data for the specified years
for year, severity in disaster_years.items():
    if year in df['Year'].values:
        df.loc[df['Year'] == year, 'Disruption'] = 1
        df.loc[df['Year'] == year, 'Severity (%)'] = severity

# Calculate the Adjusted Production (Production - Impacted Loss)
df['Production Loss (Tonnes)'] = (df['Production (Tonnes)'] * df['Severity (%)'] / 100).round(2)
df['Adjusted Production (Tonnes)'] = (df['Production (Tonnes)'] - df['Production Loss (Tonnes)']).round(2)

# Display the updated DataFrame
print(df.head())

# Save the updated DataFrame to a new CSV
output_file = 'pepper_data_with_disaster_impact.csv'
df.to_csv(output_file, index=False)
print(f"Updated data saved to: {output_file}")

# Set pandas display options to show the entire DataFrame
pd.set_option('display.max_rows', None)  # Show all rows
pd.set_option('display.max_columns', None)  # Show all columns
pd.set_option('display.width', None)  # Ensure full width is displayed
pd.set_option('display.colheader_justify', 'left')  # Align column headers

print(df)

file_path = 'pepper_data_with_disaster_impact.csv'  # Replace with your file path
df = pd.read_csv(file_path)
# Define a function to generate sentences
def create_sentence(row):
    if row['Disruption'] == 1:
        return (
            f"In {row['Year']}, the district {row['District']} had an area of {row['Area (Ha)']} hectares dedicated to pepper cultivation, "
            f"producing {row['Production (Tonnes)']} tonnes. Due to disruptions with a severity of {row['Severity (%)']}%, the production was "
            f"reduced to {row['Adjusted Production (Tonnes)']} tonnes."
        )
    else:
        return (
            f"In {row['Year']}, the district {row['District']} had an area of {row['Area (Ha)']} hectares dedicated to pepper cultivation, "
            f"producing {row['Production (Tonnes)']} tonnes without any disruptions."
        )


# Apply the function to each row
df['Description'] = df.apply(create_sentence, axis=1)

# Save the sentences to a text file for LLM training
output_file = 'pepper_data_sentences.txt'
with open(output_file, 'w') as file:
    file.write('\n'.join(df['Description']))

print(f"Data converted to sentences and saved to: {output_file}")