

**Purpose:** Transition from theory to practice.

- Build your first agent using smolagents.
    
- Start with a basic CodeAgent, then extend with tools.
    

## 🗂 Creating a Code Agent (No Tools)

**Steps:**

1. Import classes from `smolagents`.
    
2. Use the **CodeAgent** class → core of the framework.
    
3. Initialize with empty tools list.
    
4. Default model: `InferenceClientModel()` (Hugging Face).
    
5. Run with `.run(prompt)` to execute tasks.
    
6. Flexible: works with Hugging Face, OpenAI, Anthropic, etc.
    

**Outcome:** A functioning agent in just a few lines of code.

## 🗂 Why Use Tools with Code Agents?

- Base agent handles many tasks with LLM + Python.
    
- Tools extend capabilities → access external info (e.g., live web data).
    
- Essential for tasks beyond local computation.
    

## 🗂 Adding a Web Search Tool

**Process:**

- Import `WebSearchTool`.
    
- Add to agent’s tools list.
    
- Enables live search integration.
    

## 🗂 Code Agent With Web Search Tool Output

- Agent can now fetch current information.
    
- Example: run a task requiring fresh data → agent searches web, integrates results into reasoning.
    

## 🗂 Built-in Tools (by Category)

**Categories include:**

- Retrieve live info from sources.
    
- Interact with the web.
    
- Execute specific code.
    
- Interact with user.
    
- Process speech.
    
- Control workflow.
    

**Reference:** [smolagents default tools](https://huggingface.co/docs/smolagents/main/en/reference/default_tools).

## 🗂 Tools From Hugging Face Hub

- Community‑contributed tools for specialized tasks.
    
- Hosted on Hugging Face Hub.
    
- Save development time, provide ready solutions.
    

## 🗂 Using Community Tools

**Example:**

- Task: find most downloaded model for a specific task.
    
- Use `load_tool(repo_id, trust_remote_code=True)`.
    
- Add to agent’s tools list.
    
- Run with prompt: _“Find the most downloaded image classification model on Hugging Face.”_