import time

start_time = time.time()

if __name__ == "__main__":
    from src.data_loader import load_data
    from src.preprocessing import (
        clean_data, 
        fill_missing_values, 
        cap_outliers,
        encode_categorical_features, 
        scale_features
    )
    from src.model import split_data, train_model, predict_model
    from src.evaluation import evaluate_model
    from src.sequential import main_sequential
    from src.threads import main_threading
    from src.processes import main_multiprocessing

    # 1. Load dataset
    file_path = 'datasets/train.csv'
    train_data = load_data(file_path)

    # 2. Clean the dataset
    train_data_cleaned = clean_data(train_data)

    # 4. Outlier Handling: Cap outliers using the IQR method
    train_data_capped = cap_outliers(train_data_cleaned)

    # 5. Separate features (X) and target variable (y)
    X = train_data_capped.drop('SalePrice', axis=1)
    y = train_data_capped['SalePrice']

    # 6. Encode categorical features (using one-hot encoding)
    X, label_encoders = encode_categorical_features(X)

    # Display the first few rows to confirm
    print("\n---------- First Few Rows of Cleaned and Preprocessed Dataset ----------\n")
    print(X.head())

    # 7. Split the dataset into training and validation sets
    X_train, X_val, y_train, y_val = split_data(X, y)

    # 8. Fill missing values in training and validation sets
    X_train_filled, X_val_filled = fill_missing_values(X_train, X_val)

    # 9. Scale features to minimize the impact of outliers
    X_train_scaled, X_val_scaled = scale_features(X_train_filled, X_val_filled)

    # 10. Train the model on the training data
    rf_model = train_model(X_train_scaled, y_train)

    # 11. Evaluate the model (internally calls predict_model)
    rmse = evaluate_model(rf_model, X_val_scaled, y_val)
    print(f'\n---------- First Model Evaluation ----------\n\nRMSE on the validation data: {rmse}')

    # 12. Run sequential hyperparameter tuning
    best_params_seq, best_model_seq, best_rmse_seq, best_mape_seq, sequential_time = main_sequential(X_train, y_train, X_val, y_val)

    # 13. Run threaded hyperparameter tuning
    best_params_thread, best_model_thread, best_rmse_thread, best_mape_thread, threaded_time, num_threads = main_threading(X_train, y_train, X_val, y_val, 120)
    end_time_threads = time.time()
    time_threads = end_time_threads - start_time

    # 14. Run multiprocessed hyperparameter tuning
    best_params_process, best_model_process, best_rmse_process, best_mape_process, multiprocessed_time, num_processes = main_multiprocessing(X_train, y_train, X_val, y_val, 42)
    end_time_processes = time.time()
    time_processes = end_time_processes - start_time

    # 15. Compute Performance Evaluation Metrics

    # For threading
    threads_speedup = sequential_time / threaded_time
    threads_efficiency = threads_speedup / 6
    alpha_threads =  2.2256956100463867 / (time.time() - start_time)
    p_threads = 1 - alpha_threads
    threads_amdahl = 1 / ((1 - p_threads) + (p_threads / 6))
    threads_gustafson = 6 + alpha_threads * (1 - 6)

    # For multiprocessing
    processes_speedup = sequential_time / multiprocessed_time
    processes_efficiency = processes_speedup / 6
    alpha_processes = 2.209829330444336 / (time.time() - start_time) 
    p_processes = 1 - alpha_processes
    processes_amdahl = 1 / ((1 - p_processes) + (p_processes / 6))
    processes_gustafson = 6 + alpha_processes * (1 - 6)

    print("\n----------Performance Evaluation Metrics ----------\n")
    print(f"Threads Speedup: {threads_speedup}")
    print(f"Threads Efficiency: {threads_efficiency}")
    print(f"Threads Amdahl's: {threads_amdahl}")
    print(f"Threads Gustafson's: {threads_gustafson}")
    print(f"\nProcesses Speedup: {processes_speedup}")
    print(f"Processes Efficiency: {processes_efficiency}")
    print(f"Processes Amdahl's: {processes_amdahl}")
    print(f"Processes Gustafson's: {processes_gustafson}\n")