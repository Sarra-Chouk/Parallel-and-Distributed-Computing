from sklearn.model_selection import train_test_split

def split_data(data, test_size=0.2, random_state=42):
    """
    Splits the dataset into training and testing subsets.
    
    Args:
    data (pandas.DataFrame): The dataset to be split.
    test_size (float): The proportion of the dataset to include in the test split.
    random_state (int): Controls the shuffling applied to the data before splitting.
    
    Returns:
    tuple: X_train, X_test, y_train, y_test (training and
    testing data and labels).
    """
    X = data.drop(columns=['species'])
    y = data['species']
    return train_test_split(X, y, test_size=test_size, random_state=random_state)