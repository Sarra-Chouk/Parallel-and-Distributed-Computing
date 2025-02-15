from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor

def split_data(X, y, test_size=0.30, random_state=42):
    """
    Splits the dataset into training and validation sets.

    Parameters:
        X (pd.DataFrame): Feature matrix.
        y (pd.Series): Target variable.
        test_size (float): Proportion of data to be used for validation.
        random_state (int): Random seed for reproducibility.

    Returns:
        tuple: X_train, X_val, y_train, y_val
    """
    return train_test_split(X, y, test_size=test_size, random_state=random_state)

def train_model(X_train_filled, y_train, random_state=42):
    """
    Trains a Random Forest model.

    Parameters:
        X_train_filled (pd.DataFrame): Training feature matrix with missing values filled.
        y_train (pd.Series): Training target variable.
        random_state (int): Random seed for reproducibility.

    Returns:
        RandomForestRegressor: Trained model.
    """
    rf_model = RandomForestRegressor(random_state=random_state)
    rf_model.fit(X_train_filled, y_train)
    return rf_model

def predict_model(model, X_val_filled):
    """
    Makes predictions using the trained model.

    Parameters:
        model (RandomForestRegressor): Trained Random Forest model.
        X_val_filled (pd.DataFrame): Validation feature matrix with missing values filled.

    Returns:
        np.ndarray: Predicted values for the validation dataset.
    """
    return model.predict(X_val_filled)
