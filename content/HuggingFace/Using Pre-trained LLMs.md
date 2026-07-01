

**Definition:** Large Language Models (LLMs) can perform a wide variety of language tasks.

- Tasks include both **understanding** and **generation**.
    

## 🗂 Language Understanding Tasks

- Examples:
    
    - Text classification.
        
    - Sentiment analysis.
        
    - Summarization.
        
    - Question answering.
        

## 🗂 Language Generation Tasks

- Focus: **Text generation** and **Translation**.
    
- Showcase LLMs’ ability to produce new text outputs.
    
- Enhances understanding of model capabilities and structure.
    

## 🗂 Text Generation

**Process:**

- Task = `"text-generation"`.
    
- Pipeline extends user prompt (e.g., tourist destination).
    
- Parameters:
    
    - `max_length` → limit output length.
        
    - `pad_token_id = tokenizer.eos_token_id` → marks end of sequence.
        
- Output retrieved via `'generated_text'` key.
    

## 🗂 Text Generation Parameters

- **pad_token_id** → fills extra space, ensures sequences align.
    
- Marks end of meaningful text.
    
- **truncation=True** → handles inputs longer than max length.
    
- Helps model stop generating at correct point.
    

## 🗂 Guiding Output

- Prompts must be specific to avoid irrelevant results.
    
- Example: vague prompt → output about trees instead of housing.
    
- Solution: add context or combine elements (e.g., review + response in f‑string).
    
- Guides model toward coherent, relevant text.
    

## 🗂 Language Translation

**Definition:** Generate text in another language while preserving meaning.

- Hugging Face Hub supports many translation tasks.
    
- Example: English → Spanish.
    
- Task = `"translation_en_to_es"`.
    
- Parameter: `clean_up_tokenization_spaces=True` → polished output.
    
- Output retrieved via `'translation_text'` key.