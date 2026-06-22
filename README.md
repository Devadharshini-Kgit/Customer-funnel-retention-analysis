# Commerce Funnel, Retention & A/B Test Analysis

A product analytics case study analyzing user conversion behavior across the customer journey — from product view to purchase — including cohort retention tracking and a checkout A/B experiment.

**[Live Dashboard →](https://devadharshini-kgit.github.io/Customer-funnel-retention-analysis/)**

## Overview

This project simulates and analyzes e-commerce user behavior to answer three product questions:

1. **Where do users drop off in the purchase funnel?**
2. **Do customers come back after their first purchase?**
3. **Would a simplified checkout flow improve conversion?**

## Key Findings

| Metric | Result |
|---|---|
| View → Cart drop-off | 62.1% |
| Cart → Purchase drop-off | 58.2% |
| Overall conversion (view → purchase) | 15.8% |
| Month-1 cohort retention | ~30-40% |
| A/B Test: Simplified checkout lift | +12.5% (p = 0.0001, statistically significant) |

## Methodology

- **Funnel Analysis**: Tracked unique users across `view → cart → purchase` events, calculated stage-wise conversion and drop-off rates.
- **Cohort Retention**: Grouped users by signup month, measured % of purchasers returning in months M1–M3 post-signup.
- **A/B Testing**: Simulated a checkout flow experiment (3,000 users per variant) and validated the result using a two-proportion z-test at 95% confidence.

## Tech Stack

- **Python** — pandas, numpy, scipy (data generation, aggregation, statistical testing)
- **HTML/CSS/JS** — interactive dashboard visualization

## Dataset Note

This project uses a synthetically generated dataset modeled on realistic e-commerce conversion distributions (not scraped or real company data), built to demonstrate the analytical methodology used in real product analytics workflows.

## Files

- `generate_and_analyze.py` — data generation + funnel/cohort/A-B test analysis
- `index.html` — interactive dashboard
- `results.json` — raw analysis output

## Author

**Devadharshini K**
[LinkedIn](https://linkedin.com/in/devadharshini-k) · [GitHub](https://github.com/Devadharshini-Kgit)
