import pandas as pd
import json

# Define the path to your descriptions text file
file_path = 'pepper_data_sentences.txt'  # Make sure to replace this with the actual path

# Read the text file and store each line in the 'data' list
with open(file_path, 'r') as file:
    data = file.readlines()  # Reads all lines from the file into the 'data' list


# Function to process data and create input-output pairs
def process_data(data):
    formatted_data = []

    for line in data:
        # Check if there's disruption (a number following 'severity')
        if 'severity' in line:
            # Extract the year, district, and disruption severity from the sentence
            year = line.split(" ")[1]
            district = line.split("district")[1].split("had")[0].strip()
            original_production = float(line.split("producing")[1].split("tonnes")[0].strip())
            severity = float(line.split('severity of')[1].split('%')[0].strip()) / 100
            reduced_production = original_production * (1 - severity)

            # Create input-output pair for disrupted year
            formatted_data.append({
                "input": line,
                "output": f"Due to a disruption the output was reduced. The expected production is {reduced_production:.2f} tonnes."
            })
        else:
            # For non-disrupted years, just use the original production
            year = line.split(" ")[1]
            district = line.split("district")[1].split("had")[0].strip()
            original_production = float(line.split("producing")[1].split("tonnes")[0].strip())

            # Create input-output pair for non-disrupted year
            formatted_data.append({
                "input": line,
                "output": f"The expected production is {original_production:.2f} tonnes."
            })

    return formatted_data


# Process the data
processed_data = process_data(data)

# Save the output as a JSON file
with open("processed_pepper_data.json", "w") as json_file:
    json.dump(processed_data, json_file, indent=4)

print(f"Processed data saved to 'processed_pepper_data.json'")

