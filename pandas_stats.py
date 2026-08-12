import pandas as pd


# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------

filename = "2024_fb_ads_president_scored_anon.csv"


# ---------------------------------------------------------
# Load Dataset
# ---------------------------------------------------------

df = pd.read_csv(filename)


print("Dataset loaded successfully!")

print(f"Total rows: {df.shape[0]}")
print(f"Total columns: {df.shape[1]}")


# ---------------------------------------------------------
# Dataset Structure
# ---------------------------------------------------------

print("\nDataset Information")
print("-" * 50)

print("\nData Types:")
print(df.dtypes)

print("\nDataFrame Info:")
df.info()


# ---------------------------------------------------------
# Missing Values
# ---------------------------------------------------------

print("\nMissing Values")
print("-" * 50)

missing_summary = pd.DataFrame({
    "Missing Count": df.isnull().sum(),
    "Missing Percentage": (
        df.isnull().sum() / len(df)
    ) * 100
})

print(missing_summary)


# ---------------------------------------------------------
# Numeric Summary Statistics
# ---------------------------------------------------------

print("\nNumeric Summary Statistics")
print("-" * 50)

numeric_columns = df.select_dtypes(
    include="number"
).columns

print(
    df[numeric_columns].describe()
)


# ---------------------------------------------------------
# Non-Numeric Summary Statistics
# ---------------------------------------------------------

print("\nNon-Numeric Summary Statistics")
print("-" * 50)

categorical_columns = df.select_dtypes(
    exclude="number"
).columns

print(
    df[categorical_columns].describe()
)


# ---------------------------------------------------------
# Categorical Column Analysis
# ---------------------------------------------------------

print("\nCategorical Column Analysis")
print("-" * 50)


for column in categorical_columns:

    print("\n" + "=" * 60)

    print(f"Column: {column}")

    print(
        f"Unique Values: "
        f"{df[column].nunique(dropna=True)}"
    )

    print("\nTop 5 Values:")

    print(
        df[column]
        .value_counts(dropna=True)
        .head(5)
    )


# =========================================================
# GROUPED ANALYSIS BY page_id
# =========================================================

print("\n" + "#" * 70)
print("GROUPED ANALYSIS BY page_id")
print("#" * 70)


page_groups = df.groupby(
    "page_id",
    dropna=False
)


print(
    f"Number of page_id groups: "
    f"{page_groups.ngroups}"
)


# ---------------------------------------------------------
# Group Size Summary
# ---------------------------------------------------------

page_group_sizes = page_groups.size()


print(
    f"Smallest page_id group: "
    f"{page_group_sizes.min()} rows"
)

print(
    f"Largest page_id group: "
    f"{page_group_sizes.max()} rows"
)

print(
    f"Average page_id group size: "
    f"{page_group_sizes.mean():.2f} rows"
)


# ---------------------------------------------------------
# Numeric Aggregation by page_id
# ---------------------------------------------------------

print("\nNumeric Aggregation by page_id")
print("-" * 50)


page_numeric_results = (
    page_groups[numeric_columns]
    .agg([
        "count",
        "mean",
        "min",
        "max",
        "std",
        "median"
    ])
)


print(
    f"Computed numeric statistics for "
    f"{len(page_numeric_results)} page_id groups."
)


# Display only first 5 groups
print("\nSample Numeric page_id Results:")

print(
    page_numeric_results.head()
)


# ---------------------------------------------------------
# Categorical Aggregation by page_id
# ---------------------------------------------------------

print("\nCategorical Aggregation by page_id")
print("-" * 50)


page_categorical_results = {}


for column in categorical_columns:

    grouped_column = page_groups[column]

    unique_counts = grouped_column.nunique(
        dropna=True
    )

    value_counts = (
        df.groupby("page_id")[column]
        .value_counts(dropna=True)
    )

    page_categorical_results[column] = {
        "nunique": unique_counts,
        "value_counts": value_counts
    }


print(
    "Categorical grouped statistics computed "
    "for all page_id groups."
)


# ---------------------------------------------------------
# Display 5 Sample page_id Groups
# ---------------------------------------------------------

print("\nSample page_id Groups")
print("-" * 50)


sample_page_ids = list(
    page_groups.groups.keys()
)[:5]


for page_id in sample_page_ids:

    group = page_groups.get_group(
        page_id
    )

    print("\n" + "=" * 60)

    print(f"page_id: {page_id}")
    print(f"Rows in group: {len(group)}")

    print("\nNumeric Statistics:")

    print(
        group[numeric_columns].describe()
    )

    print("\nCategorical Statistics:")

    print(
        group[categorical_columns]
        .describe()
    )

    for column in categorical_columns:

        print(f"\nColumn: {column}")

        print(
            f"Unique Values: "
            f"{group[column].nunique(dropna=True)}"
        )

        print("Top 5 Values:")

        print(
            group[column]
            .value_counts(dropna=True)
            .head(5)
        )


# =========================================================
# GROUPED ANALYSIS BY page_id + ad_id
# =========================================================

print("\n" + "#" * 70)
print("GROUPED ANALYSIS BY page_id AND ad_id")
print("#" * 70)


page_ad_groups = df.groupby(
    ["page_id", "ad_id"],
    dropna=False
)


print(
    f"Number of page_id/ad_id groups: "
    f"{page_ad_groups.ngroups}"
)


# ---------------------------------------------------------
# Group Size Summary
# ---------------------------------------------------------

page_ad_group_sizes = (
    page_ad_groups.size()
)


print(
    f"Smallest page_id/ad_id group: "
    f"{page_ad_group_sizes.min()} rows"
)

print(
    f"Largest page_id/ad_id group: "
    f"{page_ad_group_sizes.max()} rows"
)

print(
    f"Average page_id/ad_id group size: "
    f"{page_ad_group_sizes.mean():.2f} rows"
)


single_row_groups = (
    page_ad_group_sizes == 1
).sum()


print(
    f"Groups containing exactly one row: "
    f"{single_row_groups}"
)


# ---------------------------------------------------------
# Numeric Aggregation by page_id + ad_id
# ---------------------------------------------------------

print("\nNumeric Aggregation by page_id and ad_id")
print("-" * 50)


page_ad_numeric_results = (
    page_ad_groups[numeric_columns]
    .agg([
        "count",
        "mean",
        "min",
        "max",
        "std",
        "median"
    ])
)


print(
    f"Computed numeric statistics for "
    f"{len(page_ad_numeric_results)} "
    f"page_id/ad_id groups."
)


print("\nSample Numeric page_id/ad_id Results:")

print(
    page_ad_numeric_results.head()
)


# ---------------------------------------------------------
# Categorical Aggregation by page_id + ad_id
# ---------------------------------------------------------

print("\nCategorical Aggregation by page_id and ad_id")
print("-" * 50)


page_ad_categorical_results = {}


for column in categorical_columns:

    unique_counts = (
        page_ad_groups[column]
        .nunique(dropna=True)
    )

    value_counts = (
        df.groupby(
            ["page_id", "ad_id"]
        )[column]
        .value_counts(dropna=True)
    )

    page_ad_categorical_results[column] = {
        "nunique": unique_counts,
        "value_counts": value_counts
    }


print(
    "Categorical grouped statistics computed "
    "for all page_id/ad_id groups."
)


# ---------------------------------------------------------
# Display 5 Sample page_id/ad_id Groups
# ---------------------------------------------------------

print("\nSample page_id/ad_id Groups")
print("-" * 50)


sample_page_ad_keys = list(
    page_ad_groups.groups.keys()
)[:5]


for page_id, ad_id in sample_page_ad_keys:

    group = page_ad_groups.get_group(
        (page_id, ad_id)
    )

    print("\n" + "=" * 60)

    print(f"page_id: {page_id}")
    print(f"ad_id: {ad_id}")
    print(f"Rows in group: {len(group)}")

    print("\nNumeric Statistics:")

    print(
        group[numeric_columns].describe()
    )

    print("\nCategorical Statistics:")

    print(
        group[categorical_columns]
        .describe()
    )

    for column in categorical_columns:

        print(f"\nColumn: {column}")

        print(
            f"Unique Values: "
            f"{group[column].nunique(dropna=True)}"
        )

        print("Top 5 Values:")

        print(
            group[column]
            .value_counts(dropna=True)
            .head(5)
        )
