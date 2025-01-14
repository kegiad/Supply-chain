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
news_article = "Heavy floods destroy crops in Idukki, causing major agricultural damage."
input_text = news_article
inputs = tokenizer(f"Classify Sentiment: {input_text}", return_tensors="pt").to(device)

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

def estimate_severity(news_article):
    high_impact_areas = ["Idukki", "Wayanad"]
    severe_events = ["flood", "drought", "landslide"]

    news_lower = news_article.lower()

    if any(area.lower() in news_lower for area in high_impact_areas):
        if any(event in news_lower for event in severe_events):
            return "High Severity"
    return "Low Severity"

if response == "negative":
    print("A disruption is predicted in the supply chain, kindly make the necessary arrangements")
    severity = estimate_severity(news_article)
    print(f"Predicted Severity: {severity}")
