import pandas as pd
import time
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

start_time = time.perf_counter()

data={
    'Age_group':['Young','Middle','Senior','Young','Middle','Senior','Young','Middle'],
    'Income': ['High','Low','Medium','Medium','High','Low','Low','High'],
    'Student': ['No','No','No','Yes','Yes','Yes','No','yes'],
    'Purchased': ['No','No','Yes','Yes','Yes','No','No','Yes']
}

df = pd.DataFrame(data)

X = df.drop(columns=['Purchased'])
Y = df['Purchased']

X_train, X_test, Y_train, Y_test = train_test_split(
    X,Y, test_size=0.25, random_state=42, stratify=Y
)

categorial_features = ['Age_group', 'Income', 'Student']
preprocessor = ColumnTransformer(
    transformers=[
        ('cat', OneHotEncoder(handle_unknown='ignore'), categorial_features)
    ]
)

model_pipline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('classifier',LogisticRegression())
])

model_pipline.fit(X_train, Y_train)

Y_pred = model_pipline.predict(X_test)

print("Accuracy:",accuracy_score(Y_test, Y_pred))
print("\nClassification Report:\n", classification_report(Y_test, Y_pred))

end_time = time.perf_counter()

execution_time = end_time - start_time

print(f"\nExecution Time: {execution_time:.6f} seconds")
print(f"Execution Time: {execution_time * 1000:.3f} milliseconds")