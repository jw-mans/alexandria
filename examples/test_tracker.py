import os
import pandas as pd
from tracker import track, log_metric, save_artifact

# создаём временную папку для артефактов
os.makedirs("runs/test_run", exist_ok=True)
os.makedirs("models", exist_ok=True)

# создаём тестовую модель (можно просто пустой файл)
with open("models/test_model.pt", "w") as f:
    f.write("dummy model content")

# создаём тестовый DataFrame
df = pd.DataFrame({
    "feature1": [1,2,3],
    "feature2": [4,5,6],
    "label": [0,1,0]
})

@track("test_experiment", artifacts_dir="runs/test_run")
def train_test_model(run_data, df):
    # логируем метрики
    log_metric(run_data, "accuracy", 0.99)
    log_metric(run_data, "loss", 0.01)

    # сохраняем артефакт
    save_artifact("models/test_model.pt", "runs/test_run", "test_model.pt")

# запускаем тест
train_test_model(df=df)
