

**Purpose:** Build agents that handle large document collections.

- Move beyond single‑prompt tasks.
    
- Enable knowledge retrieval across scattered sources.
    

## 🗂 Smart Cooking Assistant Example

**Scenario:**

- Agent helps home chefs with recipes, techniques, meal planning.
    
- Knowledge is scattered across multiple collections.
    
- Needs retrieval system to pull relevant details.
    

## 🗂 What is RAG?

**Definition:**

- Retrieval Augmented Generation = combine search + LLM.
    
- Acts like a smart librarian: scans docs, finds relevant sections, crafts answer.
    
- Bridges information retrieval with generation.
    

## 🗂 RAG Workflow

**Steps:**

1. Convert question → search query.
    
2. Find matching chunks in vector DB.
    
3. Select top 3–5 chunks.
    
4. Combine query + chunks.
    
5. Pass to LLM → generate response.
    

## 🗂 Loading and Splitting Documents

**Process:**

- Use LangChain utilities.
    
- `PyPDFDirectoryLoader("cooking_docs", mode="single")` → load PDFs.
    
- `RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)` → split into chunks.
    
- Ensures readability + preserves context.
    

## 🗂 Creating a Vector Store

**Steps:**

- Convert chunks → embeddings with `HuggingFaceEndpointEmbeddings`.
    
- Store vectors in FAISS.
    
- Enables semantic similarity search (not just keyword match).
    

## 🗂 Querying the Vector Store

**Process:**

- Use `.similarity_search()` → retrieve top 3 chunks.
    
- Join chunks into context string (separated by blank lines).
    
- Pass context + query → LLM for final answer.
    

## 🗂 Example Query: Cooking Salmon

**Illustration:**

- Query: “cooking salmon with herbs.”
    
- System retrieves related chunks: “salmon preparation,” “baking salmon in oven.”
    
- Handles semantic variation in wording.
    

## 🗂 Traditional RAG Limitations

**Challenge:**

- Complex queries (e.g., “plan a week of meals under $50 with nutrition”).
    
- Info spread across multiple docs.
    
- One‑shot search may miss details → incomplete answers.
    
- Next step: build **code agents** to overcome these gaps.