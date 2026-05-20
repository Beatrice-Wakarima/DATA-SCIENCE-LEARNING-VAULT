---
title: FastAPI — Building Data APIs
tags: [python, fastapi, apis, data-engineering]
created: 2026-05-20
up:: [[Python MOC]]
---

# ⚡ FastAPI — Building Data APIs

> FastAPI is the fastest way to build production-ready APIs in Python. Used to serve ML models, expose data pipelines, and build microservices. Powers your data products.

---

## Installation

```bash
pip install fastapi uvicorn pandas sqlalchemy python-dotenv

# Run the server
uvicorn main:app --reload --port 8000
```

---

## Your First API

```python
# main.py
from fastapi import FastAPI

app = FastAPI(
    title="Beatrice Builds Data API",
    description="API for Data Science Learning Vault",
    version="1.0.0"
)

@app.get("/")
def root():
    return {"message": "Welcome to Beatrice Builds API", "status": "running"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "version": "1.0.0"}
```

```bash
# Run it
uvicorn main:app --reload

# Visit:
# http://localhost:8000          → Root
# http://localhost:8000/docs     → Auto-generated Swagger UI!
# http://localhost:8000/redoc    → ReDoc documentation
```

---

## Path Parameters

```python
from fastapi import FastAPI, HTTPException

app = FastAPI()

# Fake database
customers_db = {
    1: {"name": "Beatrice", "tier": "Gold", "balance": 95000},
    2: {"name": "John", "tier": "Silver", "balance": 45000},
    3: {"name": "Alice", "tier": "Platinum", "balance": 250000}
}

@app.get("/customers/{customer_id}")
def get_customer(customer_id: int):
    if customer_id not in customers_db:
        raise HTTPException(status_code=404, detail=f"Customer {customer_id} not found")
    return customers_db[customer_id]

@app.get("/customers/{customer_id}/balance")
def get_balance(customer_id: int):
    if customer_id not in customers_db:
        raise HTTPException(status_code=404, detail="Customer not found")
    balance = customers_db[customer_id]["balance"]
    return {"customer_id": customer_id, "balance": balance}
```

---

## Query Parameters

```python
from typing import Optional

@app.get("/customers")
def list_customers(
    tier: Optional[str] = None,
    min_balance: Optional[float] = None,
    limit: int = 10,
    skip: int = 0
):
    """
    GET /customers?tier=Gold&min_balance=50000&limit=5
    """
    results = list(customers_db.values())
    
    if tier:
        results = [c for c in results if c["tier"] == tier]
    
    if min_balance:
        results = [c for c in results if c["balance"] >= min_balance]
    
    return {
        "total": len(results),
        "data": results[skip : skip + limit]
    }
```

---

## Request Body — Pydantic Models

```python
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

# Define data models with validation
class CustomerCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: str
    tier: str = Field(default="Bronze", pattern="^(Bronze|Silver|Gold|Platinum)$")
    initial_deposit: float = Field(default=0, ge=0)    # ge = greater or equal

class CustomerResponse(BaseModel):
    id: int
    name: str
    email: str
    tier: str
    balance: float
    created_at: datetime

class TransactionCreate(BaseModel):
    customer_id: int
    amount: float = Field(..., gt=0)    # gt = greater than
    transaction_type: str = Field(..., pattern="^(deposit|withdrawal|transfer)$")
    note: Optional[str] = None

# POST endpoint — create customer
@app.post("/customers", response_model=CustomerResponse, status_code=201)
def create_customer(customer: CustomerCreate):
    new_id = max(customers_db.keys()) + 1
    new_customer = {
        "id": new_id,
        "name": customer.name,
        "email": customer.email,
        "tier": customer.tier,
        "balance": customer.initial_deposit,
        "created_at": datetime.now()
    }
    customers_db[new_id] = new_customer
    return new_customer
```

---

## Full CRUD API

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

app = FastAPI(title="Bank Customer API")

# In-memory store (replace with database in production)
customers = {}
next_id = 1

class CustomerBase(BaseModel):
    name: str
    email: str
    tier: str = "Bronze"

class CustomerCreate(CustomerBase):
    initial_deposit: float = 0

class CustomerUpdate(BaseModel):
    name: Optional[str] = None
    tier: Optional[str] = None
    balance: Optional[float] = None

class Customer(CustomerBase):
    id: int
    balance: float
    created_at: datetime
    
    class Config:
        from_attributes = True

# CREATE
@app.post("/customers", response_model=Customer, status_code=201)
def create_customer(data: CustomerCreate):
    global next_id
    customer = {
        "id": next_id,
        "name": data.name,
        "email": data.email,
        "tier": data.tier,
        "balance": data.initial_deposit,
        "created_at": datetime.now()
    }
    customers[next_id] = customer
    next_id += 1
    return customer

# READ ALL
@app.get("/customers", response_model=List[Customer])
def get_customers(skip: int = 0, limit: int = 10):
    return list(customers.values())[skip:skip+limit]

# READ ONE
@app.get("/customers/{id}", response_model=Customer)
def get_customer(id: int):
    if id not in customers:
        raise HTTPException(404, "Customer not found")
    return customers[id]

# UPDATE
@app.patch("/customers/{id}", response_model=Customer)
def update_customer(id: int, data: CustomerUpdate):
    if id not in customers:
        raise HTTPException(404, "Customer not found")
    customer = customers[id]
    if data.name: customer["name"] = data.name
    if data.tier: customer["tier"] = data.tier
    if data.balance is not None: customer["balance"] = data.balance
    return customer

# DELETE
@app.delete("/customers/{id}")
def delete_customer(id: int):
    if id not in customers:
        raise HTTPException(404, "Customer not found")
    del customers[id]
    return {"message": f"Customer {id} deleted"}
```

---

## Serving an ML Model

```python
import pickle
import numpy as np
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Loan Prediction API")

# Load trained model (from your Loan Prediction project!)
with open("models/loan_model.pkl", "rb") as f:
    model = pickle.load(f)

class LoanApplication(BaseModel):
    age: int
    income: float
    credit_score: int
    loan_amount: float
    employment_years: float
    has_collateral: bool

class PredictionResult(BaseModel):
    approved: bool
    probability: float
    risk_level: str
    max_loan_amount: float

@app.post("/predict/loan", response_model=PredictionResult)
def predict_loan(application: LoanApplication):
    """Predict loan approval using ML model"""
    
    # Prepare features
    features = np.array([[
        application.age,
        application.income,
        application.credit_score,
        application.loan_amount,
        application.employment_years,
        int(application.has_collateral)
    ]])
    
    # Predict
    probability = float(model.predict_proba(features)[0][1])
    approved = probability >= 0.5
    
    # Risk assessment
    if probability >= 0.8:
        risk_level = "Low"
    elif probability >= 0.6:
        risk_level = "Medium"
    else:
        risk_level = "High"
    
    max_loan = application.income * 5 if approved else 0
    
    return PredictionResult(
        approved=approved,
        probability=round(probability, 4),
        risk_level=risk_level,
        max_loan_amount=max_loan
    )

@app.get("/model/info")
def model_info():
    return {
        "model_type": "RandomForestClassifier",
        "version": "1.0.0",
        "features": ["age", "income", "credit_score", "loan_amount",
                    "employment_years", "has_collateral"],
        "accuracy": 0.87
    }
```

---

## Background Tasks

```python
from fastapi import BackgroundTasks

def send_notification_email(customer_id: int, message: str):
    """Runs in background — doesn't block the response"""
    import time
    time.sleep(2)   # Simulate email sending delay
    print(f"Email sent to customer {customer_id}: {message}")

@app.post("/customers/{id}/deposit")
def make_deposit(id: int, amount: float, background_tasks: BackgroundTasks):
    if id not in customers:
        raise HTTPException(404, "Customer not found")
    
    customers[id]["balance"] += amount
    
    # Send email in background — response returns immediately
    background_tasks.add_task(
        send_notification_email,
        id,
        f"Deposit of KES {amount:,} received. New balance: KES {customers[id]['balance']:,}"
    )
    
    return {"message": "Deposit successful", "new_balance": customers[id]["balance"]}
```

---

## Middleware & CORS

```python
from fastapi.middleware.cors import CORSMiddleware
import time

app = FastAPI()

# Allow frontend to call your API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://yoursite.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Request timing middleware
@app.middleware("http")
async def add_process_time(request, call_next):
    start = time.time()
    response = await call_next(request)
    process_time = time.time() - start
    response.headers["X-Process-Time"] = str(round(process_time, 4))
    return response
```

---

## Calling Your API with Python

```python
import requests

BASE = "http://localhost:8000"

# Create customer
response = requests.post(f"{BASE}/customers", json={
    "name": "Beatrice Wakarima",
    "email": "beatrice@gmail.com",
    "tier": "Gold",
    "initial_deposit": 95000
})
customer = response.json()
print(customer)

# Get customer
response = requests.get(f"{BASE}/customers/1")
print(response.json())

# Predict loan
response = requests.post(f"{BASE}/predict/loan", json={
    "age": 28,
    "income": 120000,
    "credit_score": 720,
    "loan_amount": 500000,
    "employment_years": 5,
    "has_collateral": True
})
print(response.json())
```

---

## Quick Reference

```python
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel

app = FastAPI()

# Routes
@app.get("/path")               # GET
@app.post("/path")              # POST
@app.put("/path/{id}")          # PUT (full update)
@app.patch("/path/{id}")        # PATCH (partial update)
@app.delete("/path/{id}")       # DELETE

# Parameters
def endpoint(
    path_param: int,            # /path/123
    query_param: str = None,    # ?query=value
    body: MyModel = None        # Request body
):

# Errors
raise HTTPException(status_code=404, detail="Not found")
raise HTTPException(status_code=422, detail="Validation error")

# Status codes
201     # Created
200     # OK
204     # No content
400     # Bad request
401     # Unauthorized
403     # Forbidden
404     # Not found
500     # Server error
```

---

## Previous | Next
← [[21 - SQLAlchemy]] | → [[23 - PySpark Basics]]
