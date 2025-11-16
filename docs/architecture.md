# Alexandria — Архитектура проекта

## 1. Цель проекта
Alexandria — лёгкий инструмент для автоматического трекинга всех данных и параметров ML-тренировок.  
Он позволяет:

- фиксировать параметры, метрики, датасеты, код, окружение и артефакты
- хранить историю тренировок
- сравнивать версии моделей и datasets
- визуализировать lineage (дерево версий)

---

## 2. Логика жизненного цикла

### Шаг 1 — Разработка скрипта
```python
from tracker import track

@track(experiment_name="bert_sentiment")
def train():
    ...
```

### Шаг 2 — Сбор данных

* фиксируются параметры функции и гиперпараметры
* вычисляются хэши кода и датасета
* сохраняется окружение (Python, pip freeze, OS)

### Шаг 3 — Обучение модели

* логируются метрики с помощью `track.log_metric(key, value)`

### Шаг 4 — Завершение

* вычисляется время завершения
* сохраняются артефакты модели, графики и логи
* формируется JSON записи и отправляется на backend

### Шаг 5 — Backend

* сохраняет все данные в SQLite
* обеспечивает REST API для CLI и Web UI

### Шаг 6 — Использование

* визуализация lineage (Web UI)
* CLI команды (`trainlog diff`, `trainlog show`)
* API для анализа метрик и данных

---

## 3. Компоненты системы

| Компонент         | Технологии                              | Задачи                                                                     |
| ----------------- | --------------------------------------- | -------------------------------------------------------------------------- |
| Tracker (Python)  | Python 3.10+, hashlib, pandas, requests | Сбор параметров, хэшей, метрик, артефактов, отправка на backend            |
| Backend (FastAPI) | FastAPI, SQLAlchemy, SQLite, Pydantic   | Приём и хранение run’ов, diff engine, API                                  |
| Frontend (Web UI) | React, Tailwind, ReactFlow/Dagre        | Список запусков, lineage DAG, визуализация diff                            |
| CLI               | Python, Typer, rich                     | Быстрый доступ к run’ам, сравнение версий, просмотр датасетов и артефактов |
| Инфраструктура    | Docker, docker-compose                  | Локальный деплой backend + UI + tracker                                    |

---

## 4. REST API

### POST /runs

Создание нового run (JSON-схема run’а).

### GET /runs

Список всех run’ов (фильтры: experiment_name, tags, limit, offset).

### GET /runs/{id}

Детальная информация о run’е.

### GET /runs/{id}/diff/{other_id}

Сравнение двух run’ов (параметры, метрики, код, датасеты).

### GET /datasets

Список всех датасетов и их хэшей.

### GET /artifacts/{run_id}

Список артефактов run’а.

---

## 5. JSON-схема run’а (кратко)

```json
{
  "run_id": "uuid",
  "timestamp_start": "...",
  "timestamp_end": "...",
  "experiment_name": "...",
  "parameters": {...},
  "metrics": {...},
  "dataset": {...},
  "code": {...},
  "environment": {...},
  "artifacts": [...]
}
```

---

## 6. ER-диаграмма (текстовое описание)

```
Run
 ├── parameters (One-to-Many)
 ├── metrics (One-to-Many)
 ├── dataset (One-to-One)
 ├── code (One-to-One)
 ├── environment (One-to-One)
 └── artifacts (One-to-Many)
```