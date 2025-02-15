from math import sqrt
from sklearn.metrics import mean_squared_error
from src.model import predict_model

def evaluate_model(model, X_val_filled, y_val):
    """
    Evaluates the trained model using RMSE.

    Parameters:
        model (sklearn model): Trained model.
        X_val_filled (pd.DataFrame): Validation feature matrix with missing values filled.
        y_val (pd.Series): Validation target variable.

    Returns:
        float: Root Mean Squared Error (RMSE)
    """
    y_val_pred = predict_model(model, X_val_filled)
    rmse = sqrt(mean_squared_error(y_val, y_val_pred))
    return rmse
