

**Context:**

- Pipelines → streamlined, automatic model/tokenizer pairing.
    
- Auto classes → more customization, manual adjustments, fine‑tuning.
    

## 🗂 LLM Lifecycle

- **Phase 1: Pre‑training** → broad dataset, general language patterns.
    
- **Phase 2: Fine‑tuning** → domain‑specific data for specialized tasks.
    
- Example: insurance company fine‑tunes LLM for customer inquiries.
    

## 🗂 Loading Dataset for Fine-Tuning

**Steps:**

- Use Hugging Face **datasets library**.
    
- Example: `imdb` movie review dataset.
    
- `load_dataset("imdb", split="train")` → training data.
    
- `.shard(num_shards=4, index=0)` → split into chunks for efficiency.
    
- Adjust extraction based on computational needs.
    

## 🗂 Auto Classes for Fine-Tuning

- Common classes:
    
    - `AutoModel`
        
    - `AutoTokenizer`
        
    - Task‑specific: `AutoModelForSequenceClassification`.
        
- Load with `.from_pretrained("model_name")`.
    
- Includes learned weights + paired tokenizer.
    

## 🗂 Tokenization

**Process:**

- Select text column from dataset.
    
- Enable **padding** + **truncation** for efficiency.
    
- `return_tensors="pt"` → PyTorch tensors.
    
- Matches model’s expected input format.
    

## 🗂 Tokenization Output

- Printing shows truncated list of token IDs.
    
- Output shortened for readability in examples.
    

## 🗂 Tokenizing Row by Row

- Use `.map()` method for batch or row‑wise tokenization.
    
- `batched=True` → batch processing.
    
- Produces new dataset object with tokenized columns.
    
- Required for training loop.
    
- Note: `.map()` only accepts dataset objects, not lists.
    

## 🗂 Subword Tokenization

**Definition:** Split words into smaller meaningful parts.

- Example: “unbelievably” → `["un", "believ", "ably"]`.
    
- Common in modern tokenizers.
    
- Improves handling of rare or complex words