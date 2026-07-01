

**Definition:** Generate answers to questions about document contents.

- Inputs:
    
    - Document (PDF, contract, manual, research paper).
        
    - Question (e.g., “What is the total revenue of Q3?”).
        
- Output: direct quote or paraphrased response.
    

## 🗂 Use Cases for Document Q&A

- **Legal** → identify clauses (termination terms).
    
- **Finance** → extract figures (revenue, expenses).
    
- **Customer Support** → retrieve answers from manuals/FAQs.
    
- Automates data extraction and analysis across industries.
    

## 🗂 HR Case Study

**Scenario:**

- HR team overwhelmed with policy questions.
    
- Info stored in multi‑page PDF (US‑Employee_Policy.pdf).
    
- Document QA system retrieves answers directly.
    
- Saves HR time, streamlines communication.
    

## 🗂 Extracting Text with pypdf

**Steps:**

1. Load PDF with `PdfReader("US-Employee_Policy.pdf")`.
    
2. Access `.pages` attribute.
    
3. Iterate through pages → `.extract_text()`.
    
4. Append text into single string (`document_text`).
    

- Prepares document for Q&A pipeline.
    

## 🗂 Creating a Q&A Pipeline

**Implementation:**

- Task: `"question-answering"`.
    
- Model: `distilbert-base`.
    
- Pass question + extracted text as `context`.
    
- Example: “How many volunteer days annually?” → Answer: **1**.
    

## 🗂 Bringing It All Together

**Workflow:**

1. Extract text with `pypdf`.
    
2. Build Q&A pipeline with Hugging Face.
    
3. Pass question + document context.
    
4. Return accurate answer. **Next Step:** Wrap pipeline into reusable functions → employees ask questions directly, HR focuses on culture building.