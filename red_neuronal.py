import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
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

# Lists to store metrics for each fold (log scale)
mse_list = []
mae_list = []
r2_list = []

# Lists to store metrics for each fold (original scale)
mse_original_list = []
mae_original_list = []
r2_original_list = []

# Perform cross-validation
for train_index, test_index in rkf.split(X):
# Split data into training and test sets
    X_train, X_test = X[train_index], X[test_index]
    y_train, y_test = y[train_index], y[test_index]
    
    # Train the MLP
    mlp.fit(X_train, y_train)
    
    # Predict on the test set
    y_pred = mlp.predict(X_test)
    
    # Compute metrics in log scale
    mse = mean_squared_error(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    mse_list.append(mse)
    mae_list.append(mae)
    r2_list.append(r2)
    
    # Transform predictions back to original scale
    area_pred = np.expm1(y_pred)
    # Get original area values for test set
    area_test = raw_y.iloc[test_index].values
    
    # Compute metrics in original scale
    mse_original = mean_squared_error(area_test, area_pred)
    mae_original = mean_absolute_error(area_test, area_pred)
    r2_original = r2_score(area_test, area_pred)
    
    mse_original_list.append(mse_original)
    mae_original_list.append(mae_original)
    r2_original_list.append(r2_original)

# Compute and print the average metrics (log scale)
average_mse = np.mean(mse_list)
average_mae = np.mean(mae_list)
average_r2 = np.mean(r2_list)

print("Métricas en escala logarítmica:")
print(f'Average Mean Squared Error (log scale): {average_mse:.4f}')
print(f'Average Mean Absolute Error (log scale): {average_mae:.4f}')
print(f'Average R^2 (log scale): {average_r2:.4f}')

# Compute and print the average metrics (original scale)
average_mse_original = np.mean(mse_original_list)
average_mae_original = np.mean(mae_original_list)
average_r2_original = np.mean(r2_original_list)

print("\nMétricas en escala original:")
print(f'Average Mean Squared Error (original scale): {average_mse_original:.4f}')
print(f'Average Mean Absolute Error (original scale): {average_mae_original:.4f}')
print(f'Average R^2 (original scale): {average_r2_original:.4f}')

