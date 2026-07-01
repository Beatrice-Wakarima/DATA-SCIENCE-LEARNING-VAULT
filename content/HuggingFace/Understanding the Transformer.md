

**Purpose:** Explore how LLMs are built.

- Transformers = deep learning architectures for text processing, understanding, and generation.
    
- Handle long sequences in parallel (vs sequential).
    
- Three common structures: encoder‑only, decoder‑only, encoder‑decoder.
    

## 🗂 Transformer Architectures

- Each architecture specializes in specific tasks.
    
- Often detailed in Hugging Face model cards.
    
- Can investigate structure via model config attributes.
    

## 🗂 Encoder-only Architecture

**Focus:** Encoding + understanding input text.

- Tasks: text classification, sentiment analysis, extractive QA.
    
- Common in BERT‑based models.
    

**Identification:**

- Inspect `llm.model` or `llm.model.config`.
    
- Look for “encoder” indicators.
    
- Attributes: `is_decoder`, `is_encoder_decoder`.
    

## 🗂 Decoder-only Architecture

**Focus:** Generative output.

- Tasks: text generation, generative QA.
    
- Common in GPT‑based models.
    

**Identification:**

- Check config attributes.
    
- Sometimes `is_decoder` not explicitly set.
    
- Infer from usage (e.g., “text-generation” task).
    

## 🗂 Encoder-Decoder Architecture

**Focus:** Combine encoding + decoding.

- Tasks: language translation, text summarization.
    
- Common in T5 and BART models.
    

**Identification:**

- Inspect `llm.model` → shows encoder + decoder elements.
    
- Attribute: `is_encoder_decoder = True`.