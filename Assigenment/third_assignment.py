import pandas as pd

df1 = pd.read_csv("C:/Users/shrujal/Downloads/student_dataset_1000_rows_10_columns.csv")

print("First")
print(df1)

missing_data=df1.isnull().sum()
print("="*100)
print(missing_data)
print(missing_data[missing_data>0]if missing_data.sum()>0 else "no missing values found")

print("="*100)
print(df1.duplicated().sum())

print("="*100)
print(df1.describe().T,"\n")

print("="*100)
print(df1.describe(include=["object","category"]), "\n")

print("="*100)
categorical_col=df1.select_dtypes(include=["object","category"]).columns

for col in categorical_col:
    print(f"======={col}=======")
    print(df1[col].value_counts(),"\n")

print("="*100)
numeric_col=df1.select_dtypes(include=["number"]).columns

metrics_df=pd.DataFrame({
    'mean': df1[numeric_col].mean(),
    'Medain': df1[numeric_col].median(),
    'varience': df1[numeric_col].var(),
    'Skewness': df1[numeric_col].skew()
})
print(metrics_df)

