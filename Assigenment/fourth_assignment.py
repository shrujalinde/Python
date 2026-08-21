import pandas as pd

df=pd.read_csv("C:/Users/shrujal/Downloads/student_dataset_25.csv")
print(df)

print("="*100)
print("1. FINDING NULL VALUES")
print("="*100)
missing_data=df.isnull().sum()
print(missing_data)

print("="*100)
print("2. FINDING DUPLICATE VALUES")
print("="*100)
print("Duplicate values are: ",df.duplicated().sum())

print("="*100)
print("3. REMOVING DUPLICATE VALUES")
print("="*100)
print(df.drop_duplicates())

print("="*100)
print("4. CALCULATING MEAN FOR AGE AND SALARY ")
print("="*100)

mean_age = df["Age"].mean()
mean_salary = df["Salary"].mean()

print("Age Mean= ",mean_age)
print("Salary Mean= ",mean_salary)

print("="*100)
print("5. FILLING THE NULL VALUES AND DISPLAYING")
print("="*100)
df["Age"]=df["Age"].fillna(mean_age)
df["Salary"]=df["Salary"].fillna(mean_salary)
print(df)

print("="*100)
print("6. SPLITING THE NAME COLUMN INTO FIRST NAME AND LAST NAME ADD ADDING IT TO THE DATAFRAME")
print("="*100)
df[["First Name", "Last Name"]] = df["Student Full Name"].str.split(" ", n=1, expand=True)
print(df)

print("="*100)
print("7. REMOVING THE STUDENT FULL NAME COLUMN")
print("="*100)
df = df.drop(columns=["Student Full Name"])
print(df)

print("="*100)
print("8. NEW DATAFRAME")
print("="*100)
df = df[["First Name", "Last Name", "Age", "Salary", "Department"]]
print(df)
