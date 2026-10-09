import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

# 1. Dataset: X = Hours Studied, y = Marks Scored
X = np.array([[1], [2], [3], [4], [5], [6], [7], [8], [9], [10]])
y = np.array([35, 42, 50, 58, 65, 71, 78, 83, 90, 96])

# 2. Split dataset using scikit-learn
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 3. Train Linear Regression model using scikit-learn
model = LinearRegression()
model.fit(X_train, y_train)

# 4. Predict test set values using scikit-learn model
y_pred = model.predict(X_test)

# 5. Calculate evaluation metrics using scikit-learn
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"Marks per hour (Slope): {model.coef_[0]:.2f}")
print(f"Base marks (Intercept): {model.intercept_:.2f}")
print(f"Mean Squared Error (MSE): {mse:.2f}")
print(f"R2 Score: {r2:.4f}")

# 6. Predict marks for a new input (e.g. 7.5 study hours)
new_hours = np.array([[7.5]])
predicted_marks = model.predict(new_hours)

print(f"Predicted Marks for 7.5 hours: {predicted_marks[0]:.1f}/100")