import time
from math import sqrt
from itertools import product
from concurrent.futures import ThreadPoolExecutor, as_completed
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_percentage_error

def evaluate_params(args):
    """
    Unpacks the arguments, trains a RandomForestRegressor, evaluates it, and returns the metrics.
    """
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
    #print(f"Parameters: n_estimators={n_estimators}, max_features={max_features}, max_depth={max_depth}. RMSE: {rmse}, MAPE: {mape}%")
    
    return (rmse, mape, rf_model, {'n_estimators': n_estimators, 'max_features': max_features, 'max_depth': max_depth})

def threaded_hyperparameter_tuning(X_train, y_train, X_val, y_val, pool_size=8):
    """
    Performs hyperparameter tuning using a thread pool for a RandomForestRegressor model.
    
    Parameters:
        X_train (pd.DataFrame): Training feature matrix.
        y_train (pd.Series): Training target variable.
        X_val (pd.DataFrame): Validation feature matrix.
        y_val (pd.Series): Validation target variable.
        pool_size (int): Number of threads to run concurrently.
    
    Returns:
        dict: Best model parameters.
        RandomForestRegressor: Trained best model.
        float: Best RMSE.
        float: Best MAPE.
        float: Execution time in seconds.
        int: Total number of tasks processed.
    """
    start_time = time.time()

    # Define the parameter ranges
    n_estimators_range = [10, 25, 50, 100, 200, 300, 400]
    max_features_range = ['sqrt', 'log2', None]  # None means using all features
    max_depth_range = [1, 2, 5, 10, 20, None]      # None means no limit

    # Generate all parameter combinations
    param_combinations = list(product(n_estimators_range, max_features_range, max_depth_range))
    total_tasks = len(param_combinations)
    print(f"Starting Hyperparameter Tuning with {total_tasks} tasks using a thread pool of size {pool_size}...\n")

    # Prepare the list of arguments for each task
    args = [(n, mf, md, X_train, y_train, X_val, y_val) for n, mf, md in param_combinations]

    best_rmse = float('inf')
    best_mape = float('inf')
    best_model = None
    best_parameters = {}

    # Create a thread pool and submit tasks
    with ThreadPoolExecutor(max_workers=pool_size) as executor:
        futures = [executor.submit(evaluate_params, arg) for arg in args]
        for future in as_completed(futures):
            rmse, mape, model, parameters = future.result()
            if rmse < best_rmse:
                best_rmse = rmse
                best_mape = mape
                best_model = model
                best_parameters = parameters

    execution_time = time.time() - start_time

    print(f"\nBest Parameters: {best_parameters} | RMSE = {best_rmse}, MAPE = {best_mape}%")
    print(f"\nThreaded Execution Time: {execution_time:.2f} seconds")
    print(f"\nTotal Tasks Processed: {total_tasks}")

    return best_parameters, best_model, best_rmse, best_mape, execution_time, total_tasks

def main_threading(X_train, y_train, X_val, y_val, pool_size=50):
    """  
    Main function that handles threaded hyperparameter tuning.
    """
    print("\n---------- Running Threaded Hyperparameter Tuning ----------\n")
    best_params_thread, best_model_thread, best_rmse_thread, best_mape_thread, threaded_time, num_threads = threaded_hyperparameter_tuning(X_train, y_train, X_val, y_val, pool_size)

    return best_params_thread, best_model_thread, best_rmse_thread, best_mape_thread, threaded_time, num_threads