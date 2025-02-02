from src.data_loader import load_data
from src.preprocessing import split_data
from src.model import train_model
from src.evaluation import evaluate_model

data = load_data()
X_train, X_test, y_train, y_test = split_data(data)
model = train_model(X_train, y_train)
report = evaluate_model(model, X_test, y_test)
print(report)