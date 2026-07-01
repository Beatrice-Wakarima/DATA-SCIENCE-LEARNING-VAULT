# ETL Checklist – Excel to Postgres

## Data Source
- [ ] File names & locations
- [ ] Frequency of arrival
- [ ] Format consistency

## Schema Design
- [ ] Target schema
- [ ] Table names & column mappings
- [ ] Data types
- [ ] Keys & indexes

## Data Quality
- [ ] Missing values
- [ ] Duplicates
- [ ] Validation rules

## Transformation Logic
- [ ] Standardization
- [ ] Joins
- [ ] Derived columns
- [ ] Enrichment

## Error Handling
- [ ] Logging
- [ ] Retry policy
- [ ] Alerts

## Performance
- [ ] Batch inserts vs COPY
- [ ] Memory considerations
- [ ] Parallelization

## Reproducibility
- [ ] Dockerized
- [ ] Env vars documented
- [ ] Git version control

## Monitoring & Validation
- [ ] Row counts
- [ ] Distinct checks
- [ ] Aggregates
- [ ] Source vs target comparison
