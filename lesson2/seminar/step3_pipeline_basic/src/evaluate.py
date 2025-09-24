import pickle

import mlflow  # Import for tracking metrics
import pandas as pd
import yaml
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split


def load_params():
    with open("params.yaml", "r") as f:
        return yaml.safe_load(f)


def evaluate_model():
    params = load_params()

    with open("models/model.pkl", "rb") as f:
        model = pickle.load(f)

    df = pd.read_csv("data/processed/dataset.csv")

    X = df[["total_bill", "size"]]
    y = df["high_tip"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=params["test_size"], random_state=params["seed"]
    )

    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)

    mlflow.set_tracking_uri("file:///mlruns")
    mlflow.set_experiment("track_metrics")

    with mlflow.start_run():
        # Log parameters
        mlflow.log_params(params)

        # Log metrics
        mlflow.log_metric("accuracy", accuracy)
        mlflow.log_metric("X_train_rows", X_train.shape[0])
        mlflow.log_metric("X_test_rows", X_test.shape[0])
        mlflow.log_metric("y_train_rows", y_train.shape[0])
        mlflow.log_metric("y_test_rows", y_test.shape[0])

        # Create dict as a json for metrics
        metrics = {
            "accuracy": accuracy,
            "X_train_rows": X_train.shape[0],
            "X_test_rows": X_test.shape[0],
            "y_train_rows": y_train.shape[0],
            "y_test_rows": y_test.shape[0],
        }
        mlflow.log_dict(metrics, "metrics.json")

        print(f"Accuracy: {accuracy:.4f}")
        print(f"X_train_rows: {X_train.shape[0]}")
        print(f"X_test_rows: {X_test.shape[0]}")
        print(f"y_train_rows: {y_train.shape[0]}")
        print(f"y_test_rows: {y_test.shape[0]}")


if __name__ == "__main__":
    evaluate_model()
