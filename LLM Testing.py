import pandas as pd
import ollama

file_path = '/Users/adithyakg/anaconda3/envs/infosys_project/Infosys Project/supply_chain_sample_data.csv'

df = pd.read_csv(file_path, nrows=100000)

input_data = df.to_json(orient='records')

model_name = 'llama3.2:1b'

messages = [
    {"role": "user", "content": input_data}
]

response = ollama.chat(model=model_name, messages=messages)

print(response['message']['content'])

print("1st part completed")
print("__________________________________")

messages.append({"role": "assistant", "content": response['message']['content']})

question = "what is this data about"

messages.append({"role": "user", "content": question})

response = ollama.chat(model=model_name, messages=messages)

print(response['message']['content'])