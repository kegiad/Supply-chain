import pandas as pd
import ollama

file_path = '/Users/adithyakg/anaconda3/envs/infosys_project/Infosys Project/supply_chain_sample_data.csv'

# Load the first 1000 rows into a DataFrame
df = pd.read_csv(file_path, nrows=100000)

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
question = "what is this data about"

# Pass the data to Ollama model
response = ollama.chat(model=model_name, messages=[{"role": "user", "content": question}])

# Print the model's response
print(response['message']['content'])
