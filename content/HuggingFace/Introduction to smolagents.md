

**Purpose:** Set the stage for the course.

- Hugging Face’s lightweight framework for intelligent agents.
    
- Focus: Code Agents (smolagents’ specialty).
    
- Host welcomes learners to explore agent workflows.
    

## 🗂 Course Learning Outcomes

**By the end, you’ll be able to:**

- Understand how code agents function and why they’re powerful.
    
- Build agents that solve real-world tasks in Python.
    
- Create custom tools to extend agent capabilities.
    
- Design multi-agent workflows for complex problems.
    

## 🗂 What is an AI Agent?

**Definition:**

- System powered by a large language model.
    
- Interacts with environment to achieve user-defined objectives.
    
- Goes beyond passive chatbots → can take actions.
    

## 🗂 From Chatbots to Agents

**Key Difference:**

- Chatbots → passive responders.
    
- Agents → active actors (search web, read files, analyze data).
    
- Operate via **thought-action-observation cycle** until task completion.
    

## 🗂 Example: Competitor Pricing Research

**Scenario:**

- Agent searches company sites.
    
- Extracts pricing info.
    
- Compares and summarizes results.
    
- All triggered from a single prompt.
    

## 🗂 What is smolagents?

**Framework Overview:**

- Lightweight Python library by Hugging Face.
    
- Two agent types:
    
    - **ToolCallingAgent** → structured JSON calls.
        
    - **CodeAgent** → writes & executes Python scripts.
        
- Course focus: Code Agents.
    

## 🗂 How Function-Calling Works

**Process:**

- Predefined tools selected step-by-step.
    
- Each action = separate JSON call.
    
- Example: competitor research → multiple calls for each plan & company.
    
- Requires many individual steps.
    

## 🗂 How Code Agents Work

**Process:**

- Agent writes custom Python analysis function.
    
- Defines competitor list.
    
- Iterates with for loop, extracts pricing, stores in dictionary.
    
- Finds cheapest option with `min()`.
    
- End-to-end execution in one script.
    

## 🗂 Code Agent Flow

**Advantages:**

- Generates & executes full scripts.
    
- Combines logic, data processing, reasoning.
    
- Faster & more readable than function-calling.
    
- Research: ~20% higher success rate than traditional methods.
    
- Source: Hugging Face paper 2402.01030.