import json
import sys

import mlflow
import yaml


# Threshold from params.yaml
def load_params():
    with open("params.yaml", "r") as f:
        return yaml.safe_load(f)


# Load accuracy from metrics.json
def load_metrics():
    with open("metrics/metrics.json", "r") as f:
        return json.load(f)


params = load_params()
metrics = load_metrics()

accuracy_min = params.get("accuracy_min", 0.9)
accuracy = metrics.get("accuracy", None)

# MLFlow validation
with mlflow.start_run():
    if accuracy is None:
        print("Ошибка: accuracy не найдено в metrics.")
        mlflow.log_param("validation_status", "error")
        sys.exit(2)

    mlflow.log_metric("accuracy", accuracy)
    mlflow.log_param("accuracy_min", accuracy_min)

    if accuracy < accuracy_min:
        print(f"Провал: accuracy {accuracy} ниже порога {accuracy_min}")
        mlflow.log_param("validation_status", "fail")
        sys.exit(1)
    else:
        print(f"Успех: accuracy {accuracy} выше или равно порогу {accuracy_min}")
        mlflow.log_param("validation_status", "pass")
        sys.exit(0)
