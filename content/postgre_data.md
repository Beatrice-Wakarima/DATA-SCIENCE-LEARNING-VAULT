````
# Fundamentals of Data Models in DBMS

**Date Created:** 2025-09-28  
**Tags:** #dbms #data-modeling #postgresql #ecommerce  
**Related:** [[PostgreSQL E-commerce Dataset]], [[Database Design Principles]], [[SQL Constraints]]

---

## 🧠 Summary
Understanding data models is essential for managing databases effectively. They act as blueprints that translate business needs into technical implementations, ensuring structure, integrity, and scalability.

---

## 📌 Key Concepts

- **Data Model Definition:** Blueprint for organizing, storing, and accessing data in DBMS.
- **Translation Layer:** Bridges business requirements and technical schema.
- **Benefits of Good Modeling:**
  - Defines system scope
  - Enforces data validity
  - Supports scalability
  - Improves performance

---

## 🔍 Why Data Models Matter

- **Team Collaboration:** Aligns business analysts and developers.
- **Data Integrity:** Prevents invalid or duplicate entries.
- **Performance:** Enables efficient queries and joins.
- **Scalability:** Prepares for future growth.
- **Consistency:** Standardizes data meaning across systems.

---

## 🧱 Core Functions of a Data Model

- **Structure:** Logical organization of data.
- **Relationships:** Defines how entities interact.
- **Constraints:** Enforces business rules.
- **Abstraction:** Hides physical storage details.

---

## ⚠️ Risks Without a Data Model

- Data duplication in varied formats
- Orphaned records
- Inconsistent data interpretation
- Poor query performance

---

## 🧪 Example: Enforcing Relationships in SQL

```sql
ALTER TABLE Orders
ADD CONSTRAINT fk_customer
FOREIGN KEY (CustomerID)
REFERENCES Customer(CustomerID);
````

This constraint ensures every order is linked to a valid customer, maintaining referential integrity.

## 📚 Further Exploration

- [[Classical vs Modern Data Models]]
    
- [[Levels of Data Abstraction]]
    
- [[Advanced Optimization Strategies]]
```
# 🛒 Sample E-commerce Dataset in PostgreSQL

**Date Created:** 2025-09-28  
**Tags:** #postgresql #ecommerce #data-modeling #sql #dbms  
**Related:** [[Fundamentals of Data Models in DBMS]], [[SQL Constraints Explained]], [[Entity Relationship Diagrams]]

---

## 🧠 Summary
This note outlines the setup of a simple e-commerce dataset in PostgreSQL, used to demonstrate core data modeling concepts including entities, attributes, relationships, and constraints.

---

## 📦 Entities in the Dataset

- **Customer:** Stores buyer information.
- **Product:** Stores items available for sale.
- **Orders:** Records each purchase transaction.
- **OrderItems:** Details which products are in each order.

---

## 🔗 ER Diagram (ASCII)

```

Customer ───< Orders ───< OrderItems >─── Product

Code

````

- One customer → multiple orders  
- One order → multiple order items  
- One product → can appear in many orders

---

## 🧱 Table Schema (PostgreSQL)

```sql
CREATE TABLE Customer (
    CustomerID SERIAL PRIMARY KEY,
    CustomerName VARCHAR(100) NOT NULL,
    Email VARCHAR(100) UNIQUE NOT NULL,
    Phone VARCHAR(20),
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE Product (
    ProductID SERIAL PRIMARY KEY,
    ProductName VARCHAR(100) NOT NULL,
    Category VARCHAR(50),
    Price NUMERIC(10, 2) NOT NULL
);

CREATE TABLE Orders (
    OrderID SERIAL PRIMARY KEY,
    CustomerID INT NOT NULL,
    OrderDate DATE NOT NULL,
    Status VARCHAR(20) DEFAULT 'Pending',
    FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID)
);

CREATE TABLE OrderItems (
    OrderItemID SERIAL PRIMARY KEY,
    OrderID INT NOT NULL,
    ProductID INT NOT NULL,
    Quantity INT NOT NULL CHECK (Quantity > 0),
    FOREIGN KEY (OrderID) REFERENCES Orders(OrderID),
    FOREIGN KEY (ProductID) REFERENCES Product(ProductID)
);
````

## 📥 Sample Data Inserts

sql

```
INSERT INTO Customer (CustomerName, Email, Phone)
VALUES
('Alice Brown', 'alice@example.com', '91234567'),
('Bob McKee', 'bob@example.com', '98765432');

INSERT INTO Product (ProductName, Category, Price)
VALUES
('Laptop', 'Electronics', 1200.00),
('Wireless Mouse', 'Electronics', 25.50),
('Office Chair', 'Furniture', 150.00);

INSERT INTO Orders (CustomerID, OrderDate, Status)
VALUES
(1, '2025-08-01', 'Shipped'),
(2, '2025-08-02', 'Pending');

INSERT INTO OrderItems (OrderID, ProductID, Quantity)
VALUES
(1, 1, 1),
(1, 2, 2),
(2, 3, 1);
```

## 🧩 Key Components of a Data Model

### 1. Entities

- Represent core objects (tables): `Customer`, `Product`, `Orders`, `OrderItems`
    

### 2. Attributes

- Describe entity properties:
    
    - `CustomerName`, `Email`, `Price`, `Category`
        

### 3. Relationships

- Logical connections:
    
    - 1-to-many: `Customer` → `Orders`
        
    - Many-to-many: `Orders` ↔ `Product` via `OrderItems`
        

### 4. Constraints

- Rules for data integrity:
    
    - `UNIQUE` on `Customer.Email`
        
    - `CHECK` on `OrderItems.Quantity > 0`
        
    - `FOREIGN KEY` references for relational integrity
        

## 🛡️ Constraint Example

sql

```
CREATE TABLE OrderItems_Constraint (
    OrderItemID SERIAL PRIMARY KEY,
    OrderID INT NOT NULL,
    ProductID INT NOT NULL,
    Quantity INT NOT NULL CHECK (Quantity > 0),
    FOREIGN KEY (OrderID) REFERENCES Orders(OrderID),
    FOREIGN KEY (ProductID) REFERENCES Product(ProductID)
);
```

## 📚 Further Reading

- [[PostgreSQL Indexing Strategies]]
    
- [[Normalization vs Denormalization]]
    
- [[Designing Scalable Schemas]]