# Milestone A Reflection

## 1. Was it a challenge to produce identical numerical results across all three approaches? If so, what caused the discrepancies and how did you resolve them?

Producing consistent results across Pure Python, Pandas, and Polars required some attention because the three approaches handle data types, missing values, and statistical operations differently.

Pure Python required the most manual work. Since the CSV module reads values as strings, I had to determine whether each column was numeric or non-numeric and convert numeric values before calculating statistics. Missing values also had to be identified manually. Pandas and Polars handled much of this automatically when reading the CSV.

There were also small differences in how the libraries represented missing values and data types. For example, Pandas generally represents missing values as `NaN`, while Polars uses null values. Standard deviation can also produce unexpected results for groups containing only one record because there is not enough data to calculate a sample standard deviation.

To keep the results comparable, I used the same main statistics in all three scripts: count, mean, minimum, maximum, standard deviation, and median for numeric columns, along with count, unique values, mode, mode frequency, and top values for categorical columns.

The grouped analysis also revealed an important characteristic of the dataset. Grouping by `page_id` produced groups containing multiple advertisements, while grouping by both `page_id` and `ad_id` produced very small groups, often individual records. Because there were so many groups, printing every result was impractical. Instead, the scripts performed the grouped computations and displayed only a sample of the results.

---

## 2. Do you find one approach easier or more performant than the others? Did you measure performance, or is your assessment based on developer experience?

Pandas was the easiest approach for me to understand and use. Operations that required several loops and helper functions in Pure Python could be performed with methods such as `describe()`, `value_counts()`, `nunique()`, and `groupby()`.

Pure Python was the most difficult and verbose. However, it helped me understand what libraries such as Pandas and Polars are actually doing behind the scenes. Creating dictionaries of groups and manually calculating statistics made the grouping and aggregation process much clearer.

Polars was also concise and performed the grouped operations efficiently, but its expression-based syntax took more time to understand. I also encountered an issue when a grouping column was accidentally included twice in a `group_by()` operation. Polars' stricter handling of column names exposed the problem immediately.

My assessment is mainly based on developer experience rather than formal performance benchmarking. From this exercise, Pandas provided the best balance between readability and convenience, while Polars appeared well suited to efficient processing of larger datasets.

---

## 3. If you were coaching a junior data analyst who had never used any of these tools, what approach would you recommend they learn first? Why?

I would recommend that a junior data analyst learn **Pandas first**.

Pure Python is useful for understanding fundamental programming concepts such as loops, dictionaries, type conversion, and manual aggregation, but it requires much more code for routine data-analysis tasks. A beginner who is primarily interested in analysis may spend more time implementing basic functionality than exploring the data.

Pandas provides methods that closely match common analytical tasks. For example:

- `describe()` provides descriptive statistics.
- `value_counts()` provides frequency counts.
- `nunique()` counts unique values.
- `groupby()` makes grouped analysis much easier.

Once someone understands these concepts in Pandas, I think Polars would be a good next tool to learn. Its expression-based approach is different, but the underlying analytical concepts are similar.

I would still recommend learning enough basic Python to understand what Pandas is doing. The Pure Python portion of this milestone demonstrated why libraries such as Pandas are so useful.

---

## 4. Can coding AI tools (ChatGPT, Claude, Copilot, etc.) produce useful template code to jumpstart each approach? What do they recommend by default when asked to produce descriptive statistics? Do you agree with their recommendations?

Coding AI tools such as ChatGPT, Claude, and Copilot can provide useful starting templates for descriptive analysis. They can quickly generate examples for Pure Python, Pandas, and Polars, which can reduce the amount of time required to set up repetitive analysis code.

When asked generally to perform descriptive statistics on a CSV dataset, AI coding tools will usually suggest **Pandas first**. A typical starting point is something similar to:

```python
import pandas as pd

df = pd.read_csv("data.csv")

print(df.info())
print(df.describe())
print(df.isnull().sum())

## 5. •	Some columns in this dataset contain complex values (lists, nested structures, concatenated strings). What data cleaning was required before you could compute meaningful statistics? Did the three approaches handle this differently?

The dataset contains some columns with complex values such as lists, concatenated text, and other information stored as strings. For this milestone, I did not need to fully separate or restructure these values because the main goal was descriptive statistics and grouped analysis.

In the Pure Python approach, more manual cleaning was required. Since the `csv` module reads the data as strings, I had to identify missing values, convert numeric values to the correct type, and remove unnecessary whitespace from categorical values. Complex values were generally kept as strings and treated as categorical data.

Pandas required less manual cleaning because it automatically inferred many of the column types and handled missing values using `NaN`. Methods such as `dropna()`, `value_counts()`, and `nunique()` made it easier to work with categorical data.

Polars also inferred column types automatically and represented missing values as nulls. However, Polars uses stricter typing, so I had to be more careful about how columns were used in expressions and grouped operations.

For this milestone, complex string columns were mainly treated as complete categorical values rather than being parsed into individual components. More detailed analysis of those columns would require additional cleaning and parsing, but that was not necessary for the descriptive statistics required here.
