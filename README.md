# Supply-chain

## Description
This project uses large language models (LLMs) to optimize supply chain management by predicting inventory needs and prioritizing critical items for restocking based on external events such as natural disasters or trade disruptions.

## Features
- Predicts supply chain bottlenecks using AI.
- Prioritizes critical supplies.
- Integrates with external APIs for real-time data updates.

## Prerequisite
- Basic understanding of Large Language Models (LLMs): Familiarity with how LLMs like Meta Llama 3.2 work, including concepts like text generation, embeddings, and tokenization.
- Programming skills: Knowledge of Python and SQL.
- Basic understanding of how APIs work.

## Installation and Setup
- Install textblob for sentiment analysis, pip install textblob.
- Install requests library, to handle API requests, pip install requests.
- The APIS used here are for gathering news and supplies information.
- Download ans install Ollama for local model management.
- Download the model locally via the CLI, ollama run llama3.2:1b .
- System Requirements : 8 GB VRAM and 2 GB free space on disk recommended.
- The LLM used in this project is LLaMA 3.2 with 1B parameters.
- Install ollama library in your IDE, pip install ollama.
- Import the library and use the model llama3.2:1b .

## LLM used
- This project uses LLaMA 3.2 with 1B parameters.
- The Llama 3.2 instruction-tuned text only models are optimized for multilingual dialogue use cases, including agentic retrieval and summarization tasks. They outperform many of the available open source and closed chat models on common industry benchmarks.
- Context length : 128K tokens

## Inventory Management System
An intuitive desktop application for managing the inventory of pepper imports and exports. Built using Python and Tkinter, this system helps track inventory levels, suppliers, exporters, and logs while ensuring efficient stock management.
# Home Page
- Central hub for navigation to various modules.
- Displays inventory status and warnings for nearing capacity.
# Imports Module
- Add import records with details like supplier ID, supplier name, quantity, and price per unit.
-	Automatically calculates total cost.
-	Prevents imports that exceed inventory capacity.
# Exports Module
- Add export records with details like exporter ID, exporter name, quantity, and price per unit.
-	Automatically calculates total cost.
# Inventory Viewer
-	View and analyze inventory data in real time.
-	Provides a breakdown of imports and exports.
 # Inventory Warnings
-	Alerts when the inventory exceeds 80% of maximum capacity.
-	Prevents over-importing when inventory reaches full capacity.
