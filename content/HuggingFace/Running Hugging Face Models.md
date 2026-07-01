

**Purpose:** Move from exploring the Hub to actually using models.

- Focus: inference (prediction).
    
- Two main options: local hardware or inference providers.
    

## 🗂 Inference with Hugging Face

**Definition:**

- Inference = running models to generate predictions.
    
- Two approaches:
    
    - Local inference.
        
    - Inference providers.
        

## 🗂 Local Inference

- Run computations on personal computer or cloud dev environment.
    
- Free and convenient.
    
- Limitation: consumer hardware struggles with large LLMs, image/video generation.
    
- GPUs often required but not always available.
    

## 🗂 Inference Providers

- Remote high‑performance machines via Hugging Face API.
    
- Partner organizations run computations, return results.
    
- Faster, avoids burdening local hardware.
    
- Free credits available for Hugging Face users.
    
- Reference: [Inference providers docs](https://huggingface.co/docs/inference-providers/en/index).
    

## 🗂 Transformers Library

- Simplifies working with pre‑trained models.
    
- Supports both inference and training.
    
- Reference: [Transformers GitHub](https://github.com/huggingface/transformers).
    

## 🗂 Pipeline Class

**Steps:**

1. Import `pipeline` from transformers.
    
2. Instantiate with task + model.
    
    - Example: task = text‑generation, model = GPT‑2.
        
    - Model card: [GPT‑2](https://huggingface.co/openai-community/gpt2).
        
3. Call pipeline on input string (“What if AI”).
    
4. Returns dictionary → generated text under `'generated_text'`.
    

## 🗂 Adjusting Pipeline Parameters

- Control output length (e.g., limit to 10 tokens).
    
- Request multiple sequences (e.g., 2 outputs).
    
- Loop through results to extract generated text.
    
- Produces list of dictionaries with generated sequences.
    

## 🗂 Using Inference Providers

**Steps:**

- Create inference client → configures API communication.
    
- Specify provider (e.g., Together.ai).
    
- Provide Hugging Face API key → access credits.
    
- Perform text generation with conversational interface.
    
- Many providers available for different performance needs.