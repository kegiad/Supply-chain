from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import torch

# Device setup
device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
print(f"Using device: {device}")

# Load model and tokenizer
model_path = "./t5_nlp"
tokenizer = AutoTokenizer.from_pretrained(model_path, use_fast=True)
model = AutoModelForSeq2SeqLM.from_pretrained(model_path).to(device)

# Input with task prefix
input_text = input_text = "Global Markets Surge as Tech Giants Report Record-Breaking profits"
inputs = tokenizer(f"Classify sentiment: {input_text}", return_tensors="pt").to(device)

#inputs = tokenizer(input_text, return_tensors="pt").to(device)
print("Tokenized input:", inputs)

# Clear MPS cache
if device.type == "mps":
    torch.mps.empty_cache()

# Generate with more diversity
outputs = model.generate(
    inputs.input_ids,
    max_length=150,
    num_beams=8,
    early_stopping=True,
    no_repeat_ngram_size=3,
    do_sample=True,         # Enable sampling
    temperature=0.9,        # Controls randomness
    top_p=0.95,             # Nucleus sampling
    top_k=50                # Top-k sampling for diversity
)

# Decode outputs
raw_output = tokenizer.decode(outputs[0], skip_special_tokens=False)
print("Raw output:", raw_output)

response = tokenizer.decode(outputs[0], skip_special_tokens=True)
print("Cleaned Model response:", response)