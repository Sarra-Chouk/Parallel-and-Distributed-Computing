import multiprocessing
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

def train_model(model, X_train, y_train):
    """
    Fits the provided model on the training data.
    """
    model.fit(X_train, y_train)
    return model

def train_and_evaluate_models(dataframe):
    """
    Splits the data, trains multiple models in parallel, and evaluates their performance.
    
    Returns:
        list: A list of dictionaries with evaluation metrics for each model.
    """
    # Split data into features and target
    X = dataframe.drop(columns=['Tumor'])
    y = dataframe['Tumor']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)
    
    # Define the models
    models = [
        RandomForestClassifier(random_state=42),
        SVC(probability=True, random_state=42),
        DecisionTreeClassifier(random_state=42)
    ]
    
    # Train the models in parallel using multiprocessing
    with multiprocessing.Pool() as pool:
        trained_models = pool.starmap(train_model, [(model, X_train, y_train) for model in models])
    
    # Evaluate each model
    results = []
    for model in trained_models:
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred)
        recall = recall_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)
        cm = confusion_matrix(y_test, y_pred)
        results.append({
            'model': type(model).__name__,
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'f1_score': f1,
            'confusion_matrix': cm
        })
    return results