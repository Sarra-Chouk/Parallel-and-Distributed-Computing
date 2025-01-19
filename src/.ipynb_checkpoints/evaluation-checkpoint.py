from sklearn.metrics import classification_report

def evaluate_model(model, X_test, y_test):
    """
    Evaluates the trained model using test data and generates a classification report.
    
    Args:
    model (RandomForestClassifier): The trained machine learning model.
    X_test (pandas.DataFrame): The test features.
    y_test (pandas.Series): The test labels.
    
    Returns:
    str: A classification report as a string.
    """
    predictions = model.predict(X_test)
    return classification_report(y_test, predictions)