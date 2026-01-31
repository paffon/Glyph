# Design Log: Database Selection Research

**Date:** 2026-01-15
**Author:** Glyph AI Assistant
**Type:** Research
**Related Logs:** N/A

---
**Note:** This is a simplified example. Real design logs may be significantly longer or shorter depending on the complexity of the research.
---

## Background

Our new analytics service needs a database. Current system uses PostgreSQL for transactional data, but analytics workload has different requirements (high write throughput, time-series data, complex aggregations).

## Problem

Which database should we use for the analytics service? Need to evaluate:

- Write throughput (10k+ events/second)
- Query performance for time-series aggregations
- Operational complexity
- Cost at scale

## Questions and Answers

**Q: What types of queries will be most common?**
A: Time-range aggregations (hourly, daily, weekly), filtering by user/event type, and percentile calculations.

**Q: What's the data retention policy?**
A: Keep detailed data for 90 days, then aggregate to hourly summaries for 2 years.

**Q: What's the budget constraint?**
A: Prefer open-source to minimize licensing costs. Cloud-managed solutions acceptable if significantly reduce ops overhead.

## Design

### Research Design

Evaluated three candidates:

1. **TimescaleDB** (PostgreSQL extension)
2. **ClickHouse** (columnar OLAP)
3. **InfluxDB** (time-series database)

Methodology:

- Benchmark with 30-day sample dataset (250M events)
- Test common query patterns
- Evaluate operational complexity (setup, backup, scaling)
- Cost analysis for 1-year projection

## Plan

### Phase 1: Setup Test Environment ✅

1. Provision test infrastructure
2. Load sample dataset into each candidate
3. Create test query suite

### Phase 2: Performance Testing ✅

1. Run write throughput tests
2. Run query performance tests
3. Test retention policy implementation

### Phase 3: Operational Analysis ✅

1. Document setup complexity
2. Evaluate monitoring/alerting
3. Cost calculations

## Trade-offs

### TimescaleDB (Not Chosen)

- ✅ Familiar PostgreSQL ecosystem
- ✅ Good SQL support
- ❌ Write throughput peaked at 7k events/sec
- ❌ Query performance slower on large aggregations

### ClickHouse (Chosen)

- ✅ Excellent write throughput (15k+ events/sec)
- ✅ Fast query performance (5-10x faster than alternatives)
- ✅ Good compression (60% smaller storage)
- ❌ Different SQL dialect (learning curve)
- ❌ Limited UPDATE/DELETE support (acceptable for our use case)

### InfluxDB (Not Chosen)

- ✅ Purpose-built for time-series
- ❌ InfluxQL not standard SQL
- ❌ Enterprise features required for clustering
- ❌ Higher cost at scale

**Decision:** ClickHouse best meets performance requirements. SQL dialect differences manageable.

## Verification Criteria

- ✅ Write throughput exceeds 10k events/sec
- ✅ P95 query latency under 500ms for common queries
- ✅ Storage cost under budget ($500/month projected)
- ✅ Setup and maintenance documented

## Results

### Final Results

**Performance:**

- Write throughput: 15,200 events/sec (52% above requirement)
- P95 query latency: 320ms (36% better than target)
- Storage: 180GB for 30 days (60% compression)
- Estimated annual cost: $4,800 (within budget)

**Decision:** Proceed with ClickHouse for analytics service.

### Learnings

- Columnar storage critical for analytical workloads
- ClickHouse's SQL dialect differences minor in practice
- Compression ratios vary significantly by use case - always test with real data
- Open-source solutions can outperform commercial alternatives for specific workloads
