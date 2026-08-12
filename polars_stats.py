import polars as pl


# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------

filename = "2024_fb_ads_president_scored_anon.csv"


# ---------------------------------------------------------
# Load Dataset
# ---------------------------------------------------------

df = pl.read_csv(filename)


print("Dataset loaded successfully!")

print(f"Total rows: {df.height}")
print(f"Total columns: {df.width}")


# ---------------------------------------------------------
# Dataset Structure
# ---------------------------------------------------------

print("\nDataset Structure")
print("-" * 50)

print("\nColumn Names:")

for column in df.columns:
    print(column)


print("\nData Types:")

for column, dtype in zip(df.columns, df.dtypes):
    print(f"{column}: {dtype}")


# ---------------------------------------------------------
# Dataset-Level Summary Statistics
# ---------------------------------------------------------

print("\nDataset Summary Statistics")
print("-" * 50)

print(df.describe())


# ---------------------------------------------------------
# Missing / Null Values
# ---------------------------------------------------------

print("\nMissing / Null Values")
print("-" * 50)


null_counts = df.null_count()

print("\nNull Counts:")
print(null_counts)


print("\nNull Counts and Percentages:")

for column in df.columns:

    null_count = df[column].null_count()

    null_percentage = (
        null_count / df.height
    ) * 100

    print(
        f"{column}: "
        f"{null_count} "
        f"({null_percentage:.2f}%)"
    )


# ---------------------------------------------------------
# Identify Numeric and Categorical Columns
# ---------------------------------------------------------

numeric_columns = []
categorical_columns = []


for column, dtype in zip(df.columns, df.dtypes):

    if dtype.is_numeric():
        numeric_columns.append(column)

    else:
        categorical_columns.append(column)


print("\nNumeric Columns:")
print(numeric_columns)

print("\nCategorical Columns:")
print(categorical_columns)


# ---------------------------------------------------------
# Numeric Column Statistics
# ---------------------------------------------------------

print("\nNumeric Column Statistics")
print("-" * 50)


for column in numeric_columns:

    print("\n" + "=" * 60)
    print(f"Column: {column}")

    stats = df.select(

        pl.col(column)
        .count()
        .alias("Count"),

        pl.col(column)
        .mean()
        .alias("Mean"),

        pl.col(column)
        .min()
        .alias("Minimum"),

        pl.col(column)
        .max()
        .alias("Maximum"),

        pl.col(column)
        .std()
        .alias("Standard Deviation"),

        pl.col(column)
        .median()
        .alias("Median")
    )

    print(stats)


# ---------------------------------------------------------
# Categorical Column Statistics
# ---------------------------------------------------------

print("\nCategorical Column Statistics")
print("-" * 50)


for column in categorical_columns:

    print("\n" + "=" * 60)
    print(f"Column: {column}")

    count = (
        df[column]
        .drop_nulls()
        .len()
    )

    print(f"Count: {count}")

    unique_count = (
        df[column]
        .drop_nulls()
        .n_unique()
    )

    print(
        f"Unique Values: "
        f"{unique_count}"
    )

    value_counts = (
        df[column]
        .drop_nulls()
        .value_counts()
        .sort(
            "count",
            descending=True
        )
    )

    if value_counts.height > 0:

        mode = value_counts[0, column]

        mode_frequency = (
            value_counts[0, "count"]
        )

        print(f"Mode: {mode}")

        print(
            f"Mode Frequency: "
            f"{mode_frequency}"
        )

    print("\nTop 5 Values:")

    print(
        value_counts.head(5)
    )


# =========================================================
# GROUPED ANALYSIS BY page_id
# =========================================================

print("\n" + "#" * 70)
print("GROUPED ANALYSIS BY page_id")
print("#" * 70)


# ---------------------------------------------------------
# Group Size Summary
# ---------------------------------------------------------

page_group_sizes = (
    df.group_by("page_id")
    .agg(
        pl.len().alias("group_size")
    )
)


print(
    f"Number of page_id groups: "
    f"{page_group_sizes.height}"
)


print(
    f"Smallest page_id group: "
    f"{page_group_sizes['group_size'].min()} rows"
)


print(
    f"Largest page_id group: "
    f"{page_group_sizes['group_size'].max()} rows"
)


print(
    f"Average page_id group size: "
    f"{page_group_sizes['group_size'].mean():.2f} rows"
)


# ---------------------------------------------------------
# Numeric Aggregation by page_id
# ---------------------------------------------------------

print("\nNumeric Aggregation by page_id")
print("-" * 50)


page_numeric_expressions = []


for column in numeric_columns:

    page_numeric_expressions.extend([

        pl.col(column)
        .count()
        .alias(f"{column}_count"),

        pl.col(column)
        .mean()
        .alias(f"{column}_mean"),

        pl.col(column)
        .min()
        .alias(f"{column}_min"),

        pl.col(column)
        .max()
        .alias(f"{column}_max"),

        pl.col(column)
        .std()
        .alias(f"{column}_std"),

        pl.col(column)
        .median()
        .alias(f"{column}_median")

    ])


page_numeric_results = (
    df.group_by("page_id")
    .agg(
        page_numeric_expressions
    )
)


print(
    f"Computed numeric statistics for "
    f"{page_numeric_results.height} "
    f"page_id groups."
)


print("\nSample Numeric page_id Results:")

print(
    page_numeric_results.head(5)
)


# ---------------------------------------------------------
# Categorical Count and Unique Values by page_id
# ---------------------------------------------------------

print("\nCategorical Aggregation by page_id")
print("-" * 50)


page_categorical_results = {}


for column in categorical_columns:

    # page_id itself is already the grouping key.
    if column == "page_id":
        continue

    result = (
        df.group_by("page_id")
        .agg(

            pl.col(column)
            .count()
            .alias("count"),

            pl.col(column)
            .n_unique()
            .alias("unique_count")
        )
    )

    page_categorical_results[column] = result


print(
    "Categorical count and unique-value "
    "statistics computed for all page_id groups."
)


# ---------------------------------------------------------
# Categorical Frequencies by page_id
# ---------------------------------------------------------

page_value_counts = {}


for column in categorical_columns:

    # Avoid grouping by page_id twice.
    if column == "page_id":
        continue

    result = (
        df.group_by(
            [
                "page_id",
                column
            ]
        )
        .agg(
            pl.len()
            .alias("frequency")
        )
        .sort(
            [
                "page_id",
                "frequency"
            ],
            descending=[
                False,
                True
            ]
        )
    )

    page_value_counts[column] = result


print(
    "Categorical frequency distributions "
    "computed for all page_id groups."
)


# ---------------------------------------------------------
# Display 5 Sample page_id Groups
# ---------------------------------------------------------

print("\nSample page_id Groups")
print("-" * 50)


sample_page_ids = (
    page_group_sizes
    .select("page_id")
    .head(5)
    .to_series()
    .to_list()
)


for page_id in sample_page_ids:

    group = df.filter(
        pl.col("page_id") == page_id
    )

    print("\n" + "=" * 60)

    print(
        f"page_id: "
        f"{page_id}"
    )

    print(
        f"Rows in group: "
        f"{group.height}"
    )

    print("\nGroup Summary:")

    print(
        group.describe()
    )

    for column in categorical_columns:

        # Skip grouping identifier itself
        if column == "page_id":
            continue

        print(f"\nColumn: {column}")

        print(
            f"Unique Values: "
            f"{group[column].drop_nulls().n_unique()}"
        )

        print("Top 5 Values:")

        print(
            group[column]
            .drop_nulls()
            .value_counts()
            .sort(
                "count",
                descending=True
            )
            .head(5)
        )


# =========================================================
# GROUPED ANALYSIS BY page_id + ad_id
# =========================================================

print("\n" + "#" * 70)
print("GROUPED ANALYSIS BY page_id AND ad_id")
print("#" * 70)


# ---------------------------------------------------------
# Group Size Summary
# ---------------------------------------------------------

page_ad_group_sizes = (
    df.group_by(
        [
            "page_id",
            "ad_id"
        ]
    )
    .agg(
        pl.len()
        .alias("group_size")
    )
)


print(
    f"Number of page_id/ad_id groups: "
    f"{page_ad_group_sizes.height}"
)


print(
    f"Smallest page_id/ad_id group: "
    f"{page_ad_group_sizes['group_size'].min()} rows"
)


print(
    f"Largest page_id/ad_id group: "
    f"{page_ad_group_sizes['group_size'].max()} rows"
)


print(
    f"Average page_id/ad_id group size: "
    f"{page_ad_group_sizes['group_size'].mean():.2f} rows"
)


single_row_groups = (
    page_ad_group_sizes
    .filter(
        pl.col("group_size") == 1
    )
    .height
)


print(
    f"Groups containing exactly one row: "
    f"{single_row_groups}"
)


# ---------------------------------------------------------
# Numeric Aggregation by page_id + ad_id
# ---------------------------------------------------------

print(
    "\nNumeric Aggregation by "
    "page_id and ad_id"
)

print("-" * 50)


page_ad_numeric_expressions = []


for column in numeric_columns:

    page_ad_numeric_expressions.extend([

        pl.col(column)
        .count()
        .alias(f"{column}_count"),

        pl.col(column)
        .mean()
        .alias(f"{column}_mean"),

        pl.col(column)
        .min()
        .alias(f"{column}_min"),

        pl.col(column)
        .max()
        .alias(f"{column}_max"),

        pl.col(column)
        .std()
        .alias(f"{column}_std"),

        pl.col(column)
        .median()
        .alias(f"{column}_median")

    ])


page_ad_numeric_results = (
    df.group_by(
        [
            "page_id",
            "ad_id"
        ]
    )
    .agg(
        page_ad_numeric_expressions
    )
)


print(
    f"Computed numeric statistics for "
    f"{page_ad_numeric_results.height} "
    f"page_id/ad_id groups."
)


print(
    "\nSample Numeric "
    "page_id/ad_id Results:"
)


print(
    page_ad_numeric_results.head(5)
)


# ---------------------------------------------------------
# Categorical Count and Unique Values by page_id + ad_id
# ---------------------------------------------------------

print(
    "\nCategorical Aggregation by "
    "page_id and ad_id"
)

print("-" * 50)


page_ad_categorical_results = {}


for column in categorical_columns:

    # page_id and ad_id are already grouping keys.
    if column in ["page_id", "ad_id"]:
        continue

    result = (
        df.group_by(
            [
                "page_id",
                "ad_id"
            ]
        )
        .agg(

            pl.col(column)
            .count()
            .alias("count"),

            pl.col(column)
            .n_unique()
            .alias("unique_count")
        )
    )

    page_ad_categorical_results[column] = result


print(
    "Categorical count and unique-value "
    "statistics computed for all "
    "page_id/ad_id groups."
)


# ---------------------------------------------------------
# Categorical Frequencies by page_id + ad_id
# ---------------------------------------------------------

page_ad_value_counts = {}


for column in categorical_columns:

    # Critical fix:
    # Do not add page_id or ad_id again because
    # they are already grouping keys.
    if column in ["page_id", "ad_id"]:
        continue

    result = (
        df.group_by(
            [
                "page_id",
                "ad_id",
                column
            ]
        )
        .agg(
            pl.len()
            .alias("frequency")
        )
        .sort(
            [
                "page_id",
                "ad_id",
                "frequency"
            ],
            descending=[
                False,
                False,
                True
            ]
        )
    )

    page_ad_value_counts[column] = result


print(
    "Categorical frequency distributions "
    "computed for all page_id/ad_id groups."
)


# ---------------------------------------------------------
# Display 5 Sample page_id/ad_id Groups
# ---------------------------------------------------------

print("\nSample page_id/ad_id Groups")
print("-" * 50)


sample_keys = (
    page_ad_group_sizes
    .select(
        [
            "page_id",
            "ad_id"
        ]
    )
    .head(5)
    .rows()
)


for page_id, ad_id in sample_keys:

    group = df.filter(

        (pl.col("page_id") == page_id)

        &

        (pl.col("ad_id") == ad_id)
    )

    print("\n" + "=" * 60)

    print(
        f"page_id: "
        f"{page_id}"
    )

    print(
        f"ad_id: "
        f"{ad_id}"
    )

    print(
        f"Rows in group: "
        f"{group.height}"
    )

    print("\nGroup Summary:")

    print(
        group.describe()
    )

    for column in categorical_columns:

        # Skip the identifiers that define this group.
        if column in ["page_id", "ad_id"]:
            continue

        print(f"\nColumn: {column}")

        print(
            f"Unique Values: "
            f"{group[column].drop_nulls().n_unique()}"
        )

        print("Top 5 Values:")

        print(
            group[column]
            .drop_nulls()
            .value_counts()
            .sort(
                "count",
                descending=True
            )
            .head(5)
        )


print("\nPolars analysis completed successfully.")
