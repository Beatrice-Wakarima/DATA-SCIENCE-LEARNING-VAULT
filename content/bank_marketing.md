#  Economics Data Cleaning  **Tags:** `#economics` `#datacleaning` `#bankmarketing`

## Columns
- `client_id`: integer
- `cons_price_idx`: float
- `euribor_three_months`: float

## Output
- Saved to `economics.csv` with timestamp
- Ready for PostgreSQL import

## Related Notes
- [[Config File Design]]
- [[Raw Data Ingestion Notes]]
- [[Validation Checklist]]
#  Validation Strategy  
**Tags:** `#validation` `#pipeline` `#bankmarketing`

## Layers
- `validate_raw.py`: Run before cleaning to catch upstream issues
- `validate_outputs.py`: Run after cleaning to confirm schema and types

## Related Notes
- [[Raw Data Ingestion Notes]]
- [[Client Data Cleaning]]
- [[PostgreSQL Schema]]
#  Raw Data Validation Notes  
**Tags:** `#validation` `#rawdata` `#bankmarketing`

## Script: validate_raw.py
- Checks for missing columns
- Logs type mismatches
- Summarizes null values

## Related Notes
- [[Raw Data Ingestion Notes]]
- [[Client Data Cleaning]]
- [[Validation Strategy]]