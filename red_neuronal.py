import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import RepeatedKFold


# Load the dataset
data = pd.read_csv('forestfires.csv')

# Separate area
X = data.drop('area', axis=1)

# Transform the target variable using log(1 + area) to handle skewness
raw_y = data['area']
y = np.log1p(raw_y)

#normalize inputs between 0.0 and 1.0
scaler = MinMaxScaler()
columns_to_normalize = ['X', 'Y', 'FFMC', 'DMC', 'DC', 'ISI', 'temp', 'RH', 'wind', 'rain']
X[columns_to_normalize] = scaler.fit_transform(X[columns_to_normalize])

# One-hot encode categorical variables. Create one new column for each possible value of month and day (0,1)
X = pd.get_dummies(X, columns=['month', 'day'], drop_first=True).astype(float)

#print(X)

# Convert to numpy arrays for compatibility with sklearn
X = X.values
y = y.values


# 10-fold cross-validation repeated 30 times
rkf = RepeatedKFold(n_splits=10, n_repeats=30, random_state=42)

mlp = MLPRegressor(
    hidden_layer_sizes=(20,10,5),  
    activation='logistic',     
    solver='sgd',              
    max_iter=1000,            
    early_stopping=True,       # Stop training if validation score doesn't improve
    random_state=None          # Random initialization for each run
)

# List to store MSE for each fold
mse_list = []

# Perform cross-validation
for train_index, test_index in rkf.split(X):
    # Split data into training and test sets
    X_train, X_test = X[train_index], X[test_index]
    y_train, y_test = y[train_index], y[test_index]
    
    # Train the MLP
    mlp.fit(X_train, y_train)
    
    # Predict on the test set
    y_pred = mlp.predict(X_test)
    
    # Compute MSE and store it
    mse = mean_squared_error(y_test, y_pred)
    mse_list.append(mse)

# Compute and print the average MSE
average_mse = np.mean(mse_list)
print(f'Average Mean Squared Error: {average_mse:.4f}')

