import seaborn as sns
import matplotlib.pyplot as plt

# Load dataset
df = sns.load_dataset("penguins")
print(df.head(10))

# Remove rows containing missing values
df = df.dropna()

print(df.head(10))
print(df.info())

# Scatter plot
plt.figure(figsize=(7, 5))

sns.scatterplot(
    data=df,
    x="bill_length_mm",
    y="bill_depth_mm",
    hue="species"
)

plt.title("Scatter Plot: Bill Length vs. Bill Depth")
plt.xlabel("Bill Length (mm)")
plt.ylabel("Bill Depth (mm)")
plt.show()

# Correlation heatmap
plt.figure(figsize=(6, 5))

numeric_data = df.select_dtypes(include="number")
correlation_matrix = numeric_data.corr()

sns.heatmap(
    correlation_matrix,
    annot=True,
    cmap="coolwarm",
    fmt=".2f"
)

plt.title("Correlation Heatmap")
plt.show()