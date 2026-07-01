

**Definition:** Assign predefined categories to text.

- Common applications: reviews, social media, content moderation.
    
- Enables uncovering opinions, emotions, attitudes.
    

## 🗂 Sentiment Analysis

**Example:**

- “I love pineapple on pizza” → Positive.
    
- “I dislike pineapple on pizza” → Negative.
    
- Useful for opinion mining and customer feedback.
    

**Coding:**

- Use pipeline with `task="text-classification"`.
    
- Model labels sentiment with confidence score.
    

## 🗂 Grammatical Correctness

**Definition:** Classify text as Acceptable or Unacceptable grammar.

- “This course is great!” → Acceptable.
    
- “Course is gravy” → Unacceptable.
    

**Coding:**

- Model trained for grammar correctness.
    
- Example: “He eat pizza every day” → Incorrect grammar (LABEL_0, confidence 0.99).
    

## 🗂 Question Natural Language Inference (QNLI)

**Definition:** Check if a premise answers a question.

- Q: “What state is Hollywood in?”
    
    - Premise: “Hollywood is in California” → Entailment (True).
        
    - Premise: “Hollywood is known for its movies” → Not Entailment (False).
        

**Coding:**

- Pass question + premise separated by comma.
    
- Model outputs Entailment or Not Entailment with confidence.
    

## 🗂 Dynamic Category Assignment

**Definition:** Assign categories based on content.

- Example: “I want to know more about your pricing plans” → Sales, Marketing, Support.
    
- Model assigns confidence scores per category.
    

**Coding:**

- Use **zero-shot classification**.
    
- Example: classify newsletter request into Marketing, Sales, Support.
    
- Model predicts highest confidence label (e.g., Support).
    

## 🗂 Challenges of Text Classification

- **Ambiguity** → text with multiple meanings.
    
- **Sarcasm/Irony** → difficult to detect.
    
- **Multilingual complexity** → requires tailored processing.
    
- Solutions: advanced preprocessing + robust models.