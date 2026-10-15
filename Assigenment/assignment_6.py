import pandas as pd

file_path = r"C:/Users/shrujal/Downloads/final_student_data.csv"
df = pd.read_csv(file_path)

df.columns = df.columns.str.strip()

print("Original DataFrame:")
print(df)

print("\n" + "=" * 80)

# Concept 1
print("\nConcept 1: Average Salary & Bonus per Department\n")

dept_means = (
    df.groupby("Department")[["Salary", "Bonus_Eligible"]]
    .mean()
    .round(2)
)

print(dept_means)

print("\n" + "=" * 80)

# Concept 2
print("\nConcept 2: Average Salary & Performance by Department & Role\n")

role_hierarchy = (
    df.groupby(["Department", "Role"])[["Salary", "Performance_Rating"]]
    .mean()
    .round(2)
)

print(role_hierarchy)

print("\n" + "=" * 80)

# Concept 3
print("\nConcept 3: Advanced Aggregation\n")

dept_summary = (
    df.groupby("Department")
    .agg(
        Salary_Mean=("Salary", "mean"),
        Salary_Min=("Salary", "min"),
        Salary_Max=("Salary", "max"),
        Total_Bonus=("Bonus_Eligible", "sum"),
        Avg_Performance=("Performance_Rating", "mean")
    )
    .round(2)
)

print(dept_summary)

print("\n" + "=" * 80)

# Concept 4
print("\nConcept 4: Department Report\n")

clean_dept_report = (
    df.groupby("Department")
    .agg(
        Total_Employees=("Employee_ID", "count"),
        Total_Payroll=("Salary", "sum"),
        Average_Salary=("Salary", "mean"),
        Highest_Bonus=("Bonus_Eligible", "max"),
        Average_Performance=("Performance_Rating", "mean")
    )
    .reset_index()
    .round(2)
)

print(clean_dept_report.to_string(index=False))

print("\n" + "=" * 80)

# Concept 5
print("\nConcept 5: Departments with Payroll > 200000\n")

high_payroll_dept = df.groupby("Department").filter(
    lambda x: x["Salary"].sum() > 200000
)

result = high_payroll_dept[
    ["Department", "Full Name", "Role", "Salary"]
]

print(result.to_string(index=False))