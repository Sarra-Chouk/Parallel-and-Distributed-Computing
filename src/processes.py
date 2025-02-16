import multiprocessing
import time
from math import sqrt
from itertools import product
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_percentage_error

def evaluate_params(args):
    n_estimators, max_features, max_depth, X_train, y_train, X_val, y_val = args
    # Create and train the model
    rf_model = RandomForestRegressor(
        n_estimators=n_estimators,
        max_features=max_features,
        max_depth=max_depth,
        random_state=42
    )
    rf_model.fit(X_train, y_train)

    # Make predictions and calculate RMSE and MAPE
    y_val_pred = rf_model.predict(X_val)
    rmse = sqrt(mean_squared_error(y_val, y_val_pred))
    mape = mean_absolute_percentage_error(y_val, y_val_pred) * 100

    # Print the current combination's results
    print(f"Parameters: n_estimators={n_estimators}, max_features={max_features}, "
          f"max_depth={max_depth}. RMSE: {rmse}, MAPE: {mape}%")
    
    return (rmse, mape, rf_model, {'n_estimators': n_estimators, 'max_features': max_features, 'max_depth': max_depth})

def processes_hyperparameter_tuning(X_train, y_train, X_val, y_val, pool_size=8):
    start_time = time.time()

    # Define the parameter ranges
    n_estimators_range = [10, 25, 50, 100, 200, 300, 400]
    max_features_range = ['sqrt', 'log2', None]
    max_depth_range = [1, 2, 5, 10, 20, None]

    # Generate all parameter combinations
    param_combinations = list(product(n_estimators_range, max_features_range, max_depth_range))
    total_tasks = len(param_combinations)
    print(f"Starting Hyperparameter Tuning with {total_tasks} total tasks using a pool of {pool_size} processes...\n")

    # Prepare arguments for each task
    args = [(n, mf, md, X_train, y_train, X_val, y_val) for n, mf, md in param_combinations]

    # Create a pool of processes
    with multiprocessing.Pool(processes=pool_size) as pool:
        results = pool.map(evaluate_params, args)

    # Evaluate results
    best_rmse = float('inf')
    best_mape = float('inf')
    best_model = None
    best_parameters = {}

    for rmse, mape, model, parameters in results:
        if rmse < best_rmse:
            best_rmse = rmse
            best_mape = mape
            best_model = model
            best_parameters = parameters

    execution_time = time.time() - start_time

    print(f"\nBest Parameters: {best_parameters} | RMSE = {best_rmse}, MAPE = {best_mape}%")
    print(f"\nMultiprocessing Execution Time: {execution_time:.2f} seconds")
    print(f"\nTotal Tasks Processed: {total_tasks}")

    return best_parameters, best_model, best_rmse, best_mape, execution_time, total_tasks

def main_multiprocessing(X_train, y_train, X_val, y_val, pool_size=50):
    """
    Main function that handles multiprocessed hyperparameter tuning.
    """
    print("\n---------- Running Multiprocessed Hyperparameter Tuning ----------\n")
    best_params_process, best_model_process, best_rmse_process, best_mape_process, multiprocessed_time, num_processes = processes_hyperparameter_tuning(X_train, y_train, X_val, y_val, pool_size)

    return best_params_process, best_model_process, best_rmse_process, best_mape_process, multiprocessed_time, num_processes