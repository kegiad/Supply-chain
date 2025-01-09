import pandas as pd
import ollama

file_path = "pepper_data_with_descriptions.csv"

# Load the first 1000 rows into a DataFrame
df = pd.read_csv(file_path)

# Check the first few rows to ensure it's loaded properly
print(df.head())

# Convert the dataframe to a string representation (JSON format)
input_data = df.to_json(orient='records')

# Print the first 500 characters to check the format
print(input_data[:500])

# Define the model you want to use
model_name = 'llama3.2:1b'

# Pass the data to Ollama model
response = ollama.chat(model=model_name, messages=[{"role": "user", "content": input_data}])

# Print the model's response
print(response['message']['content'])

# Ask a new question related to the data
question = "Breaking News : A potential disruption in pepper supply is predicted. Will this impact the supply, if it does print 'Yes' otherwise print 'no' "

# Pass the data to Ollama model
response = ollama.chat(model=model_name, messages=[{"role": "user", "content": question}])
print(response['message']['content'])