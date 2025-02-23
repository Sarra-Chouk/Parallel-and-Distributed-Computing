import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, OneHotEncoder, RobustScaler
from sklearn.impute import SimpleImputer

def clean_data(data):
    """
    Clean the dataset by removing unnecessary columns.
    """
    columns_to_delete = [
        'MoSold', 'YrSold', 'SaleType', 'SaleCondition', 
        'Alley', 'FireplaceQu', 'PoolQC', 'Fence', 'MiscFeature'
    ]
    data = data.drop(columns=columns_to_delete, errors='ignore')
    return data

def cap_outliers(data, multiplier=1.5):
    """
    Cap outliers in numerical features using the IQR method.
    """
    num_cols = data.select_dtypes(include=['int64', 'float64']).columns
    for col in num_cols:
        Q1 = data[col].quantile(0.25)
        Q3 = data[col].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - multiplier * IQR
        upper_bound = Q3 + multiplier * IQR
        
        data[col] = np.where(data[col] < lower_bound, lower_bound, data[col])
        data[col] = np.where(data[col] > upper_bound, upper_bound, data[col])
    return data

def fill_missing_values(X_train, X_val):
    """
    Fill missing values. For numerical features, fill with median and for categorical
    features (if any remain) fill with mode.
    Also creates missing indicator columns.
    """
    X_train = X_train.copy()
    X_val = X_val.copy()

    num_cols = X_train.select_dtypes(include=[np.number]).columns
    cat_cols = X_train.select_dtypes(exclude=[np.number]).columns

    for col in num_cols:
        X_train[col + '_missing'] = X_train[col].isnull().astype(int)
        X_val[col + '_missing'] = X_val[col].isnull().astype(int)

        median_value = X_train[col].median()
        X_train[col] = X_train[col].fillna(median_value)
        X_val[col] = X_val[col].fillna(median_value)
    
    for col in cat_cols:
        mode_value = X_train[col].mode()[0]
        X_train[col] = X_train[col].fillna(mode_value)
        X_val[col] = X_val[col].fillna(mode_value)

    return X_train, X_val

def encode_categorical_features(X, use_onehot=True):
    """
    Encode categorical features. If use_onehot is True, performs one-hot encoding;
    otherwise, uses label encoding.
    """
    categorical_columns = X.select_dtypes(include=['object']).columns
    
    if use_onehot:
        X = pd.get_dummies(X, columns=categorical_columns, drop_first=True)
        encoders = None  
    else:
        encoders = {}
        for col in categorical_columns:
            le = LabelEncoder()
            X[col] = le.fit_transform(X[col].astype(str))
            encoders[col] = le

    return X, encoders

def scale_features(X_train, X_val):
    """
    Apply robust scaling to the features to minimize the impact of outliers.
    """
    scaler = RobustScaler()
    X_train_scaled = pd.DataFrame(scaler.fit_transform(X_train), columns=X_train.columns, index=X_train.index)
    X_val_scaled = pd.DataFrame(scaler.transform(X_val), columns=X_val.columns, index=X_val.index)
    
    return X_train_scaled, X_val_scaled