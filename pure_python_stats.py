import csv
import statistics
from collections import Counter, defaultdict


filename = "2024_fb_ads_president_scored_anon.csv"

MISSING_VALUES = {"", "NA", "N/A", "NULL", "NONE"}


def is_missing(value):
    """
    Return True if a value should be treated as missing.
    """
    if value is None:
        return True

    return value.strip().upper() in MISSING_VALUES


def infer_data_type(rows, column):
    """
    Infer whether a column is numeric or non-numeric.
    Missing values are ignored.
    """

    found_value = False

    for row in rows:
        value = row[column]

        if is_missing(value):
            continue

        found_value = True

        try:
            float(value)
        except ValueError:
            return "Non-numeric"

    if found_value:
        return "Numeric"

    return "Non-numeric"


def compute_numeric_stats(values):
    """
    Compute descriptive statistics for numeric values.
    """

    if len(values) == 0:
        return {
            "Count": 0,
            "Mean": None,
            "Minimum": None,
            "Maximum": None,
            "Standard Deviation": None,
            "Median": None
        }

    return {
        "Count": len(values),
        "Mean": statistics.mean(values),
        "Minimum": min(values),
        "Maximum": max(values),
        "Standard Deviation":
            statistics.stdev(values) if len(values) > 1 else 0,
        "Median": statistics.median(values)
    }


def compute_categorical_stats(values):
    """
    Compute descriptive statistics for non-numeric values.
    """

    if len(values) == 0:
        return {
            "Count": 0,
            "Unique Values": 0,
            "Mode": None,
            "Mode Frequency": 0,
            "Top 5 Values": []
        }

    counts = Counter(values)

    mode, frequency = counts.most_common(1)[0]

    return {
        "Count": len(values),
        "Unique Values": len(counts),
        "Mode": mode,
        "Mode Frequency": frequency,
        "Top 5 Values": counts.most_common(5)
    }


# ---------------------------------------------------------
# Load Dataset
# ---------------------------------------------------------

with open(
    filename,
    mode="r",
    encoding="utf-8-sig",
    newline=""
) as file:

    reader = csv.DictReader(file)
    data = list(reader)
    columns = reader.fieldnames


print("Dataset loaded successfully!")

print(f"Total rows: {len(data)}")
print(f"Total columns: {len(columns)}")


# ---------------------------------------------------------
# Missing Values
# ---------------------------------------------------------

print("\nMissing Values Per Column")
print("-" * 50)

missing_counts = {}

for column in columns:

    count = 0

    for row in data:

        if is_missing(row[column]):
            count += 1

    missing_counts[column] = count

    print(f"{column}: {count}")


# ---------------------------------------------------------
# Infer Data Types
# ---------------------------------------------------------

print("\nInferred Data Types")
print("-" * 50)

data_types = {}

for column in columns:

    data_types[column] = infer_data_type(
        data,
        column
    )

    print(
        f"{column}: "
        f"{data_types[column]}"
    )


# ---------------------------------------------------------
# Numeric Column Statistics
# ---------------------------------------------------------

print("\nNumeric Column Statistics")
print("-" * 50)

for column in columns:

    if data_types[column] == "Numeric":

        numeric_values = []

        for row in data:

            value = row[column]

            if is_missing(value):
                continue

            numeric_values.append(float(value))

        stats = compute_numeric_stats(
            numeric_values
        )

        print(f"\nColumn: {column}")
        print(f"Count: {stats['Count']}")
        print(f"Mean: {stats['Mean']}")
        print(f"Minimum: {stats['Minimum']}")
        print(f"Maximum: {stats['Maximum']}")
        print(
            f"Standard Deviation: "
            f"{stats['Standard Deviation']}"
        )
        print(f"Median: {stats['Median']}")


# ---------------------------------------------------------
# Non-Numeric Column Statistics
# ---------------------------------------------------------

print("\nCategorical Column Statistics")
print("-" * 50)

for column in columns:

    if data_types[column] == "Non-numeric":

        categorical_values = []

        for row in data:

            value = row[column]

            if is_missing(value):
                continue

            categorical_values.append(
                value.strip()
            )

        stats = compute_categorical_stats(
            categorical_values
        )

        print(f"\nColumn: {column}")
        print(f"Count: {stats['Count']}")
        print(
            f"Unique Values: "
            f"{stats['Unique Values']}"
        )
        print(f"Mode: {stats['Mode']}")
        print(
            f"Mode Frequency: "
            f"{stats['Mode Frequency']}"
        )

        print("Top 5 Values:")

        for value, frequency in stats["Top 5 Values"]:
            print(
                f"  {value}: {frequency}"
            )


# ---------------------------------------------------------
# Grouped Analysis
# ---------------------------------------------------------

def analyze_group(rows, columns, data_types):
    """
    Compute the same descriptive statistics for a group
    of rows as for the full dataset.
    """

    results = {}

    for column in columns:

        # Numeric columns
        if data_types[column] == "Numeric":

            numeric_values = []

            for row in rows:
                value = row[column]

                if is_missing(value):
                    continue

                numeric_values.append(float(value))

            results[column] = compute_numeric_stats(
                numeric_values
            )

        # Non-numeric columns
        else:

            categorical_values = []

            for row in rows:
                value = row[column]

                if is_missing(value):
                    continue

                categorical_values.append(
                    value.strip()
                )

            results[column] = compute_categorical_stats(
                categorical_values
            )

    return results


def print_group_result(group_name, results, data_types):
    """
    Print descriptive statistics for one group.
    """

    print("\n" + "=" * 60)
    print(group_name)
    print("=" * 60)

    for column, stats in results.items():

        print(f"\nColumn: {column}")

        if data_types[column] == "Numeric":

            print(f"Count: {stats['Count']}")
            print(f"Mean: {stats['Mean']}")
            print(f"Minimum: {stats['Minimum']}")
            print(f"Maximum: {stats['Maximum']}")

            print(
                f"Standard Deviation: "
                f"{stats['Standard Deviation']}"
            )

            print(f"Median: {stats['Median']}")

        else:

            print(f"Count: {stats['Count']}")

            print(
                f"Unique Values: "
                f"{stats['Unique Values']}"
            )

            print(f"Mode: {stats['Mode']}")

            print(
                f"Mode Frequency: "
                f"{stats['Mode Frequency']}"
            )

            print("Top 5 Values:")

            for value, frequency in stats["Top 5 Values"]:
                print(f"  {value}: {frequency}")


# =========================================================
# Grouped Analysis by page_id
# =========================================================

print("\n" + "#" * 70)
print("GROUPED ANALYSIS BY page_id")
print("#" * 70)


page_groups = defaultdict(list)

for row in data:

    page_id = row["page_id"]

    page_groups[page_id].append(row)


print(
    f"Number of page_id groups: "
    f"{len(page_groups)}"
)


# ---------------------------------------------------------
# Calculate Group Size Summary
# ---------------------------------------------------------

page_group_sizes = [
    len(rows)
    for rows in page_groups.values()
]


print(
    f"Smallest page_id group: "
    f"{min(page_group_sizes)} rows"
)

print(
    f"Largest page_id group: "
    f"{max(page_group_sizes)} rows"
)

print(
    f"Average page_id group size: "
    f"{sum(page_group_sizes) / len(page_group_sizes):.2f} rows"
)


# ---------------------------------------------------------
# Analyze ALL page_id Groups
# ---------------------------------------------------------

page_groups_analyzed = 0

page_samples = []


for page_id, rows in page_groups.items():

    # Compute full descriptive statistics
    group_results = analyze_group(
        rows,
        columns,
        data_types
    )

    page_groups_analyzed += 1

    # Keep only first 5 results for display
    if len(page_samples) < 5:

        page_samples.append(
            (
                page_id,
                len(rows),
                group_results
            )
        )


print(
    f"Completed descriptive analysis for "
    f"{page_groups_analyzed} page_id groups."
)


# ---------------------------------------------------------
# Display 5 Sample page_id Groups
# ---------------------------------------------------------

print("\nSample page_id Results")
print("-" * 50)


for page_id, row_count, results in page_samples:

    print(f"\nRows in group: {row_count}")

    print_group_result(
        f"page_id = {page_id}",
        results,
        data_types
    )


# =========================================================
# Grouped analysis by page_id + ad_id
# =========================================================

print("\n" + "#" * 70)
print("GROUPED ANALYSIS BY page_id AND ad_id")
print("#" * 70)


# Organize rows using a tuple containing
# both page_id and ad_id as the dictionary key.
page_ad_groups = defaultdict(list)


for row in data:

    group_key = (
        row["page_id"],
        row["ad_id"]
    )

    page_ad_groups[group_key].append(row)


print(
    f"Number of page_id/ad_id groups: "
    f"{len(page_ad_groups)}"
)


# ---------------------------------------------------------
# Calculate Group Size Summary
# ---------------------------------------------------------

page_ad_group_sizes = [
    len(rows)
    for rows in page_ad_groups.values()
]


print(
    f"Smallest page_id/ad_id group: "
    f"{min(page_ad_group_sizes)} rows"
)

print(
    f"Largest page_id/ad_id group: "
    f"{max(page_ad_group_sizes)} rows"
)

print(
    f"Average page_id/ad_id group size: "
    f"{sum(page_ad_group_sizes) / len(page_ad_group_sizes):.2f} rows"
)


single_row_groups = sum(
    1
    for size in page_ad_group_sizes
    if size == 1
)


print(
    f"Groups containing exactly one row: "
    f"{single_row_groups}"
)


# ---------------------------------------------------------
# Analyze ALL page_id/ad_id Groups
# ---------------------------------------------------------

page_ad_groups_analyzed = 0

page_ad_samples = []


for (page_id, ad_id), rows in page_ad_groups.items():

    # Full descriptive statistics are calculated
    # for every group.
    group_results = analyze_group(
        rows,
        columns,
        data_types
    )

    page_ad_groups_analyzed += 1

    # We keep only five results for display.
    # The remaining results are calculated but
    # immediately released from memory.
    if len(page_ad_samples) < 5:

        page_ad_samples.append(
            (
                page_id,
                ad_id,
                len(rows),
                group_results
            )
        )


print(
    f"Completed descriptive analysis for "
    f"{page_ad_groups_analyzed} page_id/ad_id groups."
)

print("\nSample page_id/ad_id Results")
print("-" * 50)


for page_id, ad_id, row_count, results in page_ad_samples:

    print(f"\nRows in group: {row_count}")

    print_group_result(
        (
            f"page_id = {page_id}, "
            f"ad_id = {ad_id}"
        ),
        results,
        data_types
    )
