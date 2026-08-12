
# Milestone A - Descriptive Statistics and Grouped Analysis

## Project Description

This milestone analyzes the `2024_fb_ads_president_scored_anon.csv` dataset using three different Python approaches:

1. **Pure Python** using only standard-library modules such as `csv`, `statistics`, and `collections`.
2. **Pandas** using DataFrames and built-in methods for descriptive statistics and grouping.
3. **Polars** using DataFrames and expression-based operations for descriptive statistics and grouping.

Each approach performs dataset-level descriptive analysis, including row and column counts, missing-value analysis, data-type identification, and statistics for numeric and non-numeric columns.

The analysis is also repeated at two grouping levels:

- Grouped by `page_id`
- Grouped by the combination of `page_id` and `ad_id`

For grouped analysis, all groups are processed, but only a small sample of the results is printed to avoid excessive terminal output.

