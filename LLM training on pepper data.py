from transformers import T5Tokenizer, T5ForConditionalGeneration
from datasets import load_dataset
from transformers import TrainingArguments
from transformers import Trainer

# Load your dataset from the JSON file
dataset = load_dataset("json", data_files="processed_pepper_data.json")

# Initialize the tokenizer
tokenizer = T5Tokenizer.from_pretrained("t5-small")

# Tokenization function for input-output pairs
def tokenize_function(examples):
    # Tokenize the 'input' text and the 'output' text (as labels)
    input_encodings = tokenizer(examples['input'], padding="max_length", truncation=True)
    output_encodings = tokenizer(examples['output'], padding="max_length", truncation=True)

    # Add the output tokenized data as labels
    input_encodings['labels'] = output_encodings['input_ids']
    return input_encodings

# Split the dataset into training and testing
train_test_split = dataset["train"].train_test_split(test_size=0.2)  # 20% for testing
tokenized_dataset = train_test_split.map(tokenize_function, batched=True)

# Ensure correct format (add 'labels' column here)
tokenized_dataset.set_format(type="torch", columns=["input_ids", "attention_mask", "labels"])

# Load the pre-trained model
model = T5ForConditionalGeneration.from_pretrained("t5-small")

# Define training arguments
training_args = TrainingArguments(
    output_dir="./results",          # Directory to save model checkpoints
    evaluation_strategy="epoch",     # Evaluate after each epoch
    per_device_train_batch_size=1,   # Batch size for training
    per_device_eval_batch_size=1,    # Batch size for evaluation
    num_train_epochs=2,              # Number of training epochs
    logging_dir="./logs",            # Directory to save logs
    logging_steps=10,                # Log every 10 steps
)

# Define the Trainer
trainer = Trainer(
    model=model,                     # The model to train
    args=training_args,              # Training arguments
    train_dataset=tokenized_dataset["train"],  # Training data
    eval_dataset=tokenized_dataset["test"],    # Evaluation data
)

# Train the model
trainer.train()