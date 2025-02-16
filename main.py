import time

start_time = time.time()

if __name__ == "__main__":
    from src.data_loader import load_data
    from src.preprocessing import clean_data, encode_categorical_features, fill_missing_values
    from src.model import split_data, train_model, predict_model
    from src.evaluation import evaluate_model
    from src.sequential import sequential_hyperparameter_tuning
    from src.threads import threaded_hyperparameter_tuning
    from src.processes import processes_hyperparameter_tuning

    # Load dataset
    file_path = 'datasets/train.csv'
    train_data = load_data(file_path)

    # Clean the dataset
    train_data_cleaned = clean_data(train_data)

    # Separate features (X) and target variable (y)
    X = train_data_cleaned.drop('SalePrice', axis=1)
    y = train_data_cleaned['SalePrice']

    # Encode categorical features
    X, label_encoders = encode_categorical_features(X)

    # Display the first few rows to confirm
    print("\n---------- First Few Rows of Cleaned and Preprocessed Dataset ----------\n")
    print(X.head())

    # Split the dataset
    X_train, X_val, y_train, y_val = split_data(X, y)

    # Fill NaN values in X_train and X_val with the median of the respective columns
    X_train_filled, X_val_filled = fill_missing_values(X_train, X_val)

    # Train the model on the training data
    rf_model = train_model(X_train_filled, y_train)

    # Evaluate model (Internally calls predict_model)
    rmse = evaluate_model(rf_model, X_val_filled, y_val)

    # Print results
    print(f'\n---------- First Model Evaluation ----------\n\nRMSE on the validation data: {rmse}')

    # Run sequential Hhperparameter tuning
    print("\n---------- Running Sequential Hyperparameter Tuning ----------\n")
    best_params_seq, best_model_seq, best_rmse_seq, best_mape_seq, sequential_time = sequential_hyperparameter_tuning(X_train, y_train, X_val, y_val)

    # Run threaded hyperparameter tuning
    print("\n---------- Running Threaded Hyperparameter Tuning ----------\n")
    best_params_thread, best_model_thread, best_rmse_thread, best_mape_thread, threaded_time, num_threads = threaded_hyperparameter_tuning(X_train, y_train, X_val, y_val, 50)
    
    end_time_threads = time.time()
    time_threads = end_time_threads - start_time # Comment Sequential hyperparameter tuning to compute this
    time_no_threads = end_time_threads - start_time # Comment sequential and threaded hyperparameter tuning to compute this
    #print(time_threads)
    #print(time_no_threads)

    # Run multiprocessed hyperparameter tuning
    print("\n---------- Running Multiprocessed Hyperparameter Tuning ----------\n")
    best_params_process, best_model_process, best_rmse_process, best_mape_process, multiprocessed_time, num_processes = processes_hyperparameter_tuning(X_train, y_train, X_val, y_val, 50)

    end_time_processes = time.time()
    time_processes = end_time_processes - start_time # Comment sequential and threaded hyperparameter tuning to compute this
    time_no_processes = end_time_processes - start_time # Comment sequential, threaded and multiprocessed hyperparameter tuning to compute this
    #print(time_processes)
    #print(time_no_processes)

    # Compute Speedup, Efficiency, Amdahl's Law, and Gustafson’s Law for threading
    threads_speedup = sequential_time / threaded_time
    threads_efficiency = threads_speedup / num_threads
    alpha_threads = 1.8289620876312256 / 24.992754459381104
    p_threads = 1 - alpha_threads
    threads_amdahl = 1 / ((1 - p_threads) + (p_threads / 6))
    threads_gustafson = 6 + alpha_threads*(1-6)

    # Compute Speedup, Efficiency, Amdahl's Law, and Gustafson’s Law for multiprocessing
    processes_speedup = sequential_time / multiprocessed_time
    processes_efficiency = processes_speedup / num_processes
    alpha_processes = 1.8289620876312256 / 15.365653991699219 # Used same total time found in threaded because negligeable difference
    p_processes = 1 - alpha_processes
    processes_amdahl = 1 / ((1 - p_processes) + (p_processes / 6))
    processes_gustafson = 6 + alpha_processes*(1-6)

    print("\n----------Performance Evaluation Metrics ----------\n")
    print(f"Threads Speedup: {threads_speedup}")
    print(f"Threads Efficiency: {threads_efficiency}")
    print(f"Threads Amdahl's: {threads_amdahl}")
    print(f"Threads Gustafson's: {threads_gustafson}")
    print(f"\nProcesses Speedup: {processes_speedup}")
    print(f"Processes Efficiency: {processes_efficiency}")
    print(f"Processes Amdahl's: {processes_amdahl}")
    print(f"Processes Gustafson's: {processes_gustafson}\n")