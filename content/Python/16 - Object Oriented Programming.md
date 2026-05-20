---
title: Object Oriented Programming (OOP)
tags: [python, oop, advanced]
created: 2026-05-20
up:: [[Python MOC]]
---

# 🏗️ Object Oriented Programming (OOP)

> OOP lets you model real-world things as objects — bundling data (attributes) and behaviour (methods) together. Essential for building pipelines, APIs, and production-grade code.

---

## Why OOP?

```python
# Without OOP — messy, hard to scale
customer_name = "Beatrice"
customer_balance = 95000
customer_tier = "Gold"

def deposit(balance, amount):
    return balance + amount

# With OOP — clean, reusable, scalable
class Customer:
    def __init__(self, name, balance):
        self.name = name
        self.balance = balance
    
    def deposit(self, amount):
        self.balance += amount
```

---

## Classes and Objects

```python
# Class = Blueprint
class Customer:
    
    # Constructor — runs when object is created
    def __init__(self, name, account_number, balance=0):
        self.name = name                    # Attribute
        self.account_number = account_number
        self.balance = balance
        self.transactions = []              # Empty list
    
    # Method — behaviour
    def deposit(self, amount):
        self.balance += amount
        self.transactions.append(f"+{amount}")
        print(f"✅ Deposited KES {amount:,}. New balance: KES {self.balance:,}")
    
    def withdraw(self, amount):
        if amount > self.balance:
            print("❌ Insufficient funds")
        else:
            self.balance -= amount
            self.transactions.append(f"-{amount}")
            print(f"✅ Withdrew KES {amount:,}. New balance: KES {self.balance:,}")
    
    def get_statement(self):
        print(f"\n📄 Statement for {self.name}")
        print(f"Account: {self.account_number}")
        print(f"Balance: KES {self.balance:,}")
        print(f"Transactions: {self.transactions}")
    
    # String representation
    def __str__(self):
        return f"Customer({self.name}, KES {self.balance:,})"

# Create objects (instances)
beatrice = Customer("Beatrice Wakarima", "ACC001", 50000)
john = Customer("John Doe", "ACC002", 25000)

# Use methods
beatrice.deposit(45000)
beatrice.withdraw(10000)
beatrice.get_statement()

print(beatrice)             # Customer(Beatrice Wakarima, KES 85,000)
```

---

## Class Attributes vs Instance Attributes

```python
class BankAccount:
    
    # Class attribute — shared by ALL instances
    bank_name = "Beatrice Bank"
    interest_rate = 0.08
    total_accounts = 0
    
    def __init__(self, owner, balance):
        # Instance attributes — unique to each object
        self.owner = owner
        self.balance = balance
        BankAccount.total_accounts += 1     # Increment class counter
    
    def add_interest(self):
        interest = self.balance * BankAccount.interest_rate
        self.balance += interest
        return interest

# All accounts share bank_name
acc1 = BankAccount("Beatrice", 100000)
acc2 = BankAccount("John", 50000)

print(BankAccount.bank_name)        # Beatrice Bank
print(BankAccount.total_accounts)   # 2
print(acc1.bank_name)               # Beatrice Bank (inherited)
```

---

## Inheritance — Building on Existing Classes

```python
# Parent class
class Account:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance
    
    def deposit(self, amount):
        self.balance += amount
        print(f"Deposited KES {amount:,}")
    
    def __str__(self):
        return f"{self.__class__.__name__}({self.owner}: KES {self.balance:,})"


# Child classes — inherit from Account
class SavingsAccount(Account):
    def __init__(self, owner, balance=0, interest_rate=0.08):
        super().__init__(owner, balance)    # Call parent __init__
        self.interest_rate = interest_rate
    
    def add_interest(self):
        interest = self.balance * self.interest_rate
        self.balance += interest
        print(f"Interest added: KES {interest:,.2f}")
        return interest


class LoanAccount(Account):
    def __init__(self, owner, principal, rate=0.15):
        super().__init__(owner, balance=-principal)  # Negative balance = debt
        self.principal = principal
        self.rate = rate
    
    def monthly_payment(self):
        return (self.principal * self.rate) / 12
    
    def make_payment(self, amount):
        self.balance += amount
        print(f"Payment of KES {amount:,} made. Remaining: KES {abs(self.balance):,}")


class PremiumAccount(SavingsAccount):
    """Premium inherits from Savings which inherits from Account"""
    def __init__(self, owner, balance=0):
        super().__init__(owner, balance, interest_rate=0.12)   # Higher rate
        self.relationship_manager = None
        self.perks = ["Airport lounge", "Zero transfer fees", "Priority support"]
    
    def assign_manager(self, manager_name):
        self.relationship_manager = manager_name
        print(f"Assigned {manager_name} as relationship manager")


# Use them
savings = SavingsAccount("Beatrice", 100000)
loan = LoanAccount("John", 500000)
premium = PremiumAccount("Alice", 250000)

savings.deposit(50000)
savings.add_interest()

loan.make_payment(10000)
print(f"Monthly payment: KES {loan.monthly_payment():,.2f}")

premium.assign_manager("David Kamau")
premium.add_interest()
print(premium.perks)

print(savings)          # SavingsAccount(Beatrice: KES 162,000)
print(loan)             # LoanAccount(John: KES -490,000)
print(premium)          # PremiumAccount(Alice: KES 280,000)
```

---

## Encapsulation — Protecting Data

```python
class Employee:
    def __init__(self, name, salary):
        self.name = name
        self.__salary = salary      # __ = private attribute
    
    # Getter
    @property
    def salary(self):
        return self.__salary
    
    # Setter — with validation
    @salary.setter
    def salary(self, amount):
        if amount < 0:
            raise ValueError("Salary cannot be negative")
        if amount < 30000:
            raise ValueError("Salary below minimum wage")
        self.__salary = amount
    
    def get_annual_package(self):
        return self.__salary * 12 + (self.__salary * 0.1 * 12)  # salary + 10% bonus

emp = Employee("Beatrice", 120000)
print(emp.salary)           # 120000 (via getter)
emp.salary = 135000         # Uses setter (with validation)

try:
    emp.salary = -5000      # Raises ValueError
except ValueError as e:
    print(f"Error: {e}")
```

---

## Real World Example — Data Pipeline as OOP

```python
import pandas as pd
from pathlib import Path

class DataPipeline:
    """Production-grade data pipeline using OOP"""
    
    def __init__(self, name, source_path, output_path):
        self.name = name
        self.source_path = Path(source_path)
        self.output_path = Path(output_path)
        self.df = None
        self.logs = []
        self._log(f"Pipeline '{name}' initialized")
    
    def _log(self, message):
        """Private logging method"""
        from datetime import datetime
        entry = f"[{datetime.now().strftime('%H:%M:%S')}] {message}"
        self.logs.append(entry)
        print(entry)
    
    def extract(self):
        """Load data from source"""
        self._log(f"Extracting from {self.source_path}")
        self.df = pd.read_csv(self.source_path)
        self._log(f"Extracted {len(self.df):,} rows")
        return self
    
    def transform(self):
        """Clean and transform data"""
        self._log("Transforming data...")
        
        # Clean strings
        if "name" in self.df.columns:
            self.df["name"] = self.df["name"].str.strip().str.title()
        
        # Remove duplicates
        before = len(self.df)
        self.df = self.df.drop_duplicates()
        self._log(f"Removed {before - len(self.df)} duplicates")
        
        # Handle nulls
        self.df = self.df.dropna()
        self._log(f"Final rows: {len(self.df):,}")
        return self
    
    def load(self, filename):
        """Save processed data"""
        self.output_path.mkdir(parents=True, exist_ok=True)
        out = self.output_path / filename
        self.df.to_csv(out, index=False)
        self._log(f"Saved to {out}")
        return self
    
    def run(self, output_filename="output.csv"):
        """Run full ETL pipeline"""
        self._log(f"🚀 Starting pipeline: {self.name}")
        self.extract().transform().load(output_filename)
        self._log(f"✅ Pipeline complete!")
        return self.df
    
    def __str__(self):
        rows = len(self.df) if self.df is not None else 0
        return f"Pipeline({self.name}: {rows} rows)"


# Use the pipeline
pipeline = DataPipeline(
    name="Bank Marketing ETL",
    source_path="data/bank_marketing.csv",
    output_path="outputs/cleaned"
)

result = pipeline.run("bank_marketing_clean.csv")
print(pipeline)
```

---

## OOP Cheatsheet

```python
class MyClass:
    class_var = "shared"                    # Class attribute
    
    def __init__(self, x):                  # Constructor
        self.x = x                          # Instance attribute
        self.__private = "hidden"           # Private attribute
    
    def method(self):                       # Instance method
        return self.x
    
    @classmethod
    def class_method(cls):                  # Class method
        return cls.class_var
    
    @staticmethod
    def static_method():                    # Static method (no self/cls)
        return "utility function"
    
    @property
    def value(self):                        # Getter
        return self.__private
    
    @value.setter
    def value(self, v):                     # Setter
        self.__private = v
    
    def __str__(self):                      # String representation
        return f"MyClass({self.x})"
    
    def __len__(self):                      # len() support
        return self.x
    
    def __eq__(self, other):                # == comparison
        return self.x == other.x


class Child(MyClass):                       # Inheritance
    def __init__(self, x, y):
        super().__init__(x)                 # Call parent
        self.y = y
```

---

## Previous | Next
← [[15 - File Handling]] | → [[17 - Error Handling and Logging]]
