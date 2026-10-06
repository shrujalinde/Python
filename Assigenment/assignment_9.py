import pandas as pd
import numpy as np
from scipy import stats
data ={
    'Study_Hours' : [2,3,5,7,9,4,8,6,10,1],
    'Exam_Score' : [55,60,72,81,93,65,88,76,98,50]

}

df = pd.DataFrame(data)

x = df['Study_Hours']

mean_val = np.mean(x)
median_val=np.median(x)

# variance_val = np.var(x , ddof=1)
# std_val = np.std(x , ddof=1)
variance_val = np.var(x)
std_val = np.std(x)

print(f"Mean: {mean_val}")
print(f"Median: {median_val}")
print(f"Simple Varience: {variance_val}")
print(f"Standard Deviation: {std_val}")

pearson_corr, p_value = stats.pearsonr(df['Study_Hours'], df['Exam_Score'])

print(f"Pearson Correlation: {pearson_corr: .4f}")
print(f"P_value: {p_value: .4f}\n")


print("-----Pandas Summary Stats-----")
print(df.describe())

print("\n ===== Correlaton Matrix =====")
print(df.corr())