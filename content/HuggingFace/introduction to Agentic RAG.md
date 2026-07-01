

**Purpose:** Move beyond traditional RAG pipelines.

- Blend retrieval with iterative reasoning.
    
- Agents refine queries until they gather enough evidence.
    

## 🗂 Agentic RAG: Iterative Retrieval + Reasoning

**Process:**

- Agent retrieves initial results.
    
- Spots gaps in evidence.
    
- Issues refined queries.
    
- Continues until answer is complete.
    
- Wrap similarity search into a custom tool for flexibility.
    

## 🗂 Stateless vs Stateful Tools

- **Stateless tools** → function‑based, no memory between calls.
    
- **Stateful tools** → class‑based, inherit from `Tool`.
    
- Maintain references to complex objects (e.g., vector stores).
    
- Required for iterative retrieval workflows.
    

## 🗂 Anatomy of a Class-Based Tool

**Structure:**

- **Name** → identifies tool.
    
- **Description** → explains purpose.
    
- **Inputs** → parameters with types.
    
- **output_type** → defines return format.
    
- `.__init__()` → sets persistent state (e.g., vector store).
    
- `super().__init__()` → initialize parent Tool class.
    
- `.forward()` → contains logic executed by agent.
    

## 🗂 Recipe Search Tool

**Implementation:**

- Name, description, inputs, output type defined.
    
- `.__init__()` → keeps vector store reference, sets `k=6` docs.
    
- `.forward()` → performs similarity search, joins results with `\n\n`.
    
- Returns “Nothing found.” if no matches.
    
- Provides readable, separated text blocks.
    

## 🗂 Cooking Assistant Agent

**Setup:**

- **instructions** → system prompt guiding thorough search.
    
- **verbosity_level** → controls output detail:
    
    - 0 → final answer only.
        
    - 1 → reasoning steps + tool calls.
        
    - 2 → full debugging output.
        
- **max_steps** → prevents infinite loops.
    
- Agent searches multiple times if needed.
    

## 🗂 Agent Run Example

**Outcome:**

- Agent thoroughly examines cooking documentation.
    
- Provides complete, evidence‑based answers.
    
- Demonstrates iterative retrieval + reasoning in action.