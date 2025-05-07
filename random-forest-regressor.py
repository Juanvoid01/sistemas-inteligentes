import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn import svm
from sklearn.metrics import mean_squared_error, r2_score


# Load dataset
df = pd.read_csv('forestfires.csv')

# Target
target = 'area'

# Separate features and target
X = df.drop(columns=[target])
y = df[target]
y = np.log1p(y)

# Define categorical and numerical columns
categorical = ['month', 'day']
numerical = [col for col in X.columns if col not in categorical]

# Preprocess
preprocessor = ColumnTransformer([
    ('cat', OneHotEncoder(), categorical),
    ('num', StandardScaler(), numerical)
])
X_processed = preprocessor.fit_transform(X)

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X_processed, y, test_size=0.2, random_state=0)

# Initialize and train Random Forest Regressor
rf = RandomForestRegressor(random_state=0)
# rf = svm.SVR()
rf.fit(X_train, y_train)

# Predict on the test set
y_pred = rf.predict(X_test)

# Evaluate the tuned model
print("Random Forest RMSE:", mean_squared_error(y_test, y_pred))
print("Random Forest R2 Score:", r2_score(y_test, y_pred))
