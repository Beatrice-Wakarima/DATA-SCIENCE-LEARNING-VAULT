

**Definition:** Reduce large text into smaller, concise form while retaining key information.

- Common NLP task for clarity and efficiency.
    

## 🗂 Extractive vs Abstractive Summarization

- **Extractive** → selects key sentences from input.
    
    - Efficient, resource‑light.
        
    - May lack cohesion/readability.
        
- **Abstractive** → generates new text capturing main ideas.
    
    - Flexible, natural summaries.
        
    - Requires more computation, may introduce fabrications.
        

## 🗂 Use Cases: Extractive Summarization

- **Legal Document Analysis** → highlight key clauses.
    
- **Financial Research** → extract main insights.
    
- Focus: accuracy, no fabricated content.
    

## 🗂 Use Cases: Abstractive Summarization

- **News Article Summaries** → concise, readable overviews.
    
- **Content Recommendations** → compelling descriptions.
    
- Focus: clarity, engagement, impact.
    

## 🗂 Extractive Summarization in Action

**Pipeline:**

python

```
from transformers import pipeline
summarizer = pipeline("summarization", model="extractive-model")
summary = summarizer(long_text)
```

- Output: dictionary with summarized text.
    
- Preserves phrasing, selects factual sentences.
    

## 🗂 Abstractive Summarization in Action

**Pipeline:**

python

```
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
summary = summarizer(long_text)
```

- Generates new, concise, readable text.
    
- May introduce fabrications not in original input.
    

## 🗂 Parameters for Summarization

- **min_new_tokens** → minimum length of summary.
    
- **max_new_tokens** → maximum length of summary.
    
- Tokens = units of text (words/characters).
    
- Control verbosity, ensure concise + meaningful output.