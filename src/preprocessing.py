import pandas as pd
from sklearn.preprocessing import LabelEncoder

def clean_data(data):
    """
    Clean the dataset by removing unnecessary columns.

    Parameters:
        data (pd.DataFrame): The input dataset.

    Returns:
        pd.DataFrame: Cleaned dataset.
    """
    columns_to_delete = ['MoSold', 'YrSold', 'SaleType', 'SaleCondition', 'Alley', 'FireplaceQu', 'PoolQC', 'Fence', 'MiscFeature']
    return data.drop(columns=columns_to_delete, axis=1)

def encode_categorical_features(X):
    """
    Encode categorical features in the dataset.

    Parameters:
        X (pd.DataFrame): Feature matrix with categorical variables.

    Returns:
        pd.DataFrame: Transformed feature matrix.
        dict: Dictionary of fitted LabelEncoders for each categorical column.
    """
    categorical_columns = X.select_dtypes(include=['object']).columns
    label_encoders = {column: LabelEncoder() for column in categorical_columns}

    for column in categorical_columns:
        X[column] = label_encoders[column].fit_transform(X[column])

    return X, label_encoders

def fill_missing_values(X_train, X_val):
    """
    Fill NaN values with the median of respective columns.

    Parameters:
        X_train (pd.DataFrame): Training feature matrix.
        X_val (pd.DataFrame): Validation feature matrix.

    Returns:
        tuple: X_train_filled, X_val_filled
    """
    X_train_filled = X_train.fillna(X_train.median())
    X_val_filled = X_val.fillna(X_val.median())
    return X_train_filled, X_val_filled