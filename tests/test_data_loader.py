from src.data_loader import load_data

def test_load_data():
    """
    Tests whether the dataset is loaded correctly and is not empty.
    """
    data = load_data()
    assert not data.empty, "Data should not be empty"