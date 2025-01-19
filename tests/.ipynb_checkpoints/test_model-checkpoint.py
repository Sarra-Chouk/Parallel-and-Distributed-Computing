from src.model import train_model
from src.data_loader import load_data
from src.preprocessing import split_data

def test_train_model():
    """
    Tests whether the RandomForestClassifier is trained correctly.
    """
    data = load_data()
    X_train, _, y_train, _ = split_data(data)
    model = train_model(X_train, y_train)
    assert model is not None, "Model should not be None"
    assert hasattr(model, "predict"), "Model should have a predict method"