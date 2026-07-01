How our data pipeline flows conceptually. Because our script reads multiple distinct staging inputs, runs isolated processing tracks, and relies on strict dependencies (dimensions must be fully committed before the fact table can safely map its foreign keys), our transformation pipeline executes as a Directed Acyclic Graph (DAG).

```
   [stg_fact_sales]      [stg_dim_customers]      [stg_dim_products]      [stg_state_region]
          │                       │                       │                       │
          ▼                       ▼                       ▼                       ▼
   ┌──────────────┐        ┌──────────────┐        ┌──────────────┐        ┌──────────────┐
   │  T1: Parse   │        │  T2: Clean   │        │  T4: Coerce  │        │  T2: Clean   │
   │  Timestamps  │        │ State Codes  │        │   Numerics   │        │ State Codes  │
   └──────┬───────┘        └──────┬───────┘        └──────┬───────┘        └──────┬───────┘
          │                       │                       │                       │
          │                       ▼                       │                       │
          │                ┌──────────────┐               │                       │
          │                │ T2b: Vector  │               │                       │
          │                │  Postal Mode │               │                       │
          │                └──────┬───────┘               │                       │
          │                       │                       │                       │
          ▼                       ▼                       │                       │
   ┌──────────────┐        ┌──────────────┐               │                       │
   │ T5: Extrap.  │        │ T3: Dedupe   │               │                       │
   │  Min/Max Dt  │        │  Customers   │               │                       │
   └──────┬───────┘        └──────┬───────┘               │                       │
          │                       │                       │                       │
          │                       ├───────────────────────┼───────────────────────┘
          │                       │                       │
          │                       ▼                       ▼
          │                ┌──────────────┐        ┌──────────────┐
          │                │   T6 & T8:   │        │   T7: Load   │
          │                │ Merge Region │        │ Canonical    │
          │                │ & Enrich Cust│        │ dim_products │
          │                └──────┬───────┘        └──────┬───────┘
          │                       │                       │
          ▼                       ▼                       ▼
   ┌──────────────┐        ┌──────────────┐        ┌──────────────┐
   │ Write Target │        │ Write Target │        │ Write Target │
   │ dw.dim_date  │        │dw.dim_cust...│        │dw.dim_prod...│
   └──────┬───────┘        └──────┬───────┘        └──────┬───────┘
          │                       │                       │
          └───────────────────────┼───────────────────────┘
                                  │
                                  ▼ (Requires all Dimension FKs to exist)
                           ┌──────────────┐
                           │   T9: Map    │
                           │ Cost/Margin  │
                           │ & Align Keys │
                           └──────┬───────┘
                                  │
                                  ▼
                           ┌──────────────┐
                           │ Write Target │
                           │ dw.fact_sales│
                           └──────────────┘
```

### DAG Node Breakdown & Execution Sequence

1. **Extraction / Source Layer (Independent Parallel Scans):**
    
    - The pipeline extracts four distinct staging matrices simultaneously via `read_staging`: `stg_fact_sales`, `stg_dim_customers`, `stg_dim_products`, and `stg_geo`.
        
2. **Cleanse & Structural Mutation Vectors:**
    
    - **`stg_fact_sales` Track:** Parses timestamps vectorially (**T1**). The output min/max dates are captured to form the operational boundaries for the date spine (**T5**).
        
    - **Customer & Geography Track:** Runs uppercase normalization over state abbreviations (**T2**), processes complex US Postal patterns through C-allocated conditional logic (**T2b**), and strips structural duplicates (**T3**).
        
    - **Product Track:** Coerces metrics into steady `float`/`int` layouts (**T4**).
        
3. **Dimensional Join & Enrichment Layer:**
    
    - The deduplicated customer dataset is combined with the geographic state lookup tables via an implicit relational vector map (**T6** & **T8**).
        
    - Unknown geographic bounds are handled with robust fallback values.
        
4. **Ordered Warehouse Streaming Layer (The Integrity Gate):**
    
    - **Dimensions First:** `dw.dim_date`, `dw.dim_products`, and `dw.dim_customers` are targeted first. Their primary database rows are wiped (`CASCADE`) and bulk-streamed to guarantee constraint validity downstream.
        
    - **Fact Table Last:** Once `dim_products` is locked into the warehouse destination, `stg_sales` is combined with it vectorially to extract cost data, dynamically compute gross margins, resolve foreign keys, and write to `dw.fact_sales` (**T9**).