

**Purpose:** Explore datasets alongside models.

- Community‑curated across diverse tasks/domains.
    
- Accessible under the **Datasets tab**.
    
- Reference: [Datasets Hub](https://huggingface.co/datasets).
    

## 🗂 Filtering Datasets

- Apply filters (modality, task, keywords).
    
- Similar process to filtering models.
    
- Enables quick discovery of suitable datasets.
    

## 🗂 Italian Text Generation Example

**Scenario:**

- Goal: fine‑tune text generation model for Italian.
    
- Filters: Text modality → Text Generation task.
    
- Narrow further with keyword search.
    
- Select promising dataset from results.
    

## 🗂 Dataset Cards

**Contents:**

- Compilation details.
    
- License information.
    
- Number of rows.
    
- Preview via dataset viewer.
    
- Deeper exploration with **Data Studio**.
    

## 🗂 SQL Queries in Data Studio

- Manipulate datasets directly.
    
- Example:
    
    sql
    
    ```
    SELECT * FROM dataset WHERE text LIKE '%bella%'
    ```
    
- Filters rows containing “bella” (“beautiful” in Italian).
    
- Once satisfied, move to Python for further work.
    

## 🗂 Datasets Python Package

- Hugging Face **datasets** library.
    
- Minimal code to access, download, use, share datasets.
    
- Reference: [Datasets loading docs](https://huggingface.co/docs/datasets/loading).
    

## 🗂 Downloading a Dataset

**Function:**

python

```
from datasets import load_dataset
dataset = load_dataset("dataset_path", split="train")
```

- Parameters: `split` → train, test, validate.
    
- Check dataset card for available partitions.
    
- Reference: [Loading guide](https://huggingface.co/docs/datasets/v2.15.0/loading).
    

## 🗂 Apache Arrow Format

- Columnar storage format.
    
- Faster querying vs row‑based storage.
    
- Widely used in Hugging Face datasets.
    
- Reference: [Apache Arrow overview](https://arrow.apache.org/overview/).
    

## 🗂 Data Manipulation: Filter

**Method:**

python

```
dataset.filter(lambda row: "bella" in row["text"])
```

- Applies criteria to each row.
    
- Returns filtered dataset.
    
- Reference: [Filter docs](https://huggingface.co/docs/datasets/process#select-and-filter).
    

## 🗂 Data Manipulation: Select

**Method:**

python

```
subset = dataset.select(range(2))
print(subset[0]["text"])
```

- Select rows by index.
    
- Example: first two rows.
    
- Access specific entry by row index + column.
    
- Reference: [Select docs](https://huggingface.co/docs/datasets/process#select-and-filter).