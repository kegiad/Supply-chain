import pandas as pd
from transformers import T5Tokenizer
from datasets import Dataset
from transformers import T5ForConditionalGeneration, Trainer, TrainingArguments

# Load your CSV dataset
df = pd.read_csv('combined_sentiment_data.csv')

# Display the first few rows to check the structure
print(df.head())

# Format the data for T5
df['input_text'] = 'Classify sentiment: ' + df['sentence']
df['output_text'] = df['sentiment']

# Display the formatted data
print(df[['input_text', 'output_text']].head())

# Load the tokenizer
tokenizer = T5Tokenizer.from_pretrained("t5-small")

# Tokenize the data
def tokenize_data(examples):
    model_inputs = tokenizer(examples['input_text'], max_length=512, truncation=True, padding='max_length')
    labels = tokenizer(examples['output_text'], max_length=2, truncation=True, padding='max_length')
    model_inputs['labels'] = labels['input_ids']
    return model_inputs

# Apply tokenization to your dataset
tokenized_data = df.apply(tokenize_data, axis=1)

# You can now use this tokenized data for training

# Convert to Hugging Face Dataset format
dataset = Dataset.from_pandas(df)

# Use `map` to tokenize the dataset
tokenized_dataset = dataset.map(tokenize_data, batched=True)

# Load the model
model = T5ForConditionalGeneration.from_pretrained("t5-small")

# Define the training arguments
training_args = TrainingArguments(
    output_dir='./results',
    evaluation_strategy="epoch",
    learning_rate=2e-5,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    num_train_epochs=3,
    weight_decay=0.01,
    logging_dir='./logs',
)

# Define the Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset,
    eval_dataset=tokenized_dataset,  # If you have a separate eval dataset, use it here
)

# Start training
trainer.train()
# Save the model and tokenizer to a directory named 't5_nlp'
model.save_pretrained('t5_nlp')
tokenizer.save_pretrained('t5_nlp')
