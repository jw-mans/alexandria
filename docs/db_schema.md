# Alexandria — Схема базы данных

База данных: SQLite  
ORM: SQLAlchemy

---

## Таблицы и связи

### 1. Run
| Поле | Тип | Описание |
|------|-----|----------|
| id | UUID / INTEGER PK | Уникальный идентификатор run’а |
| experiment_name | STRING | Название эксперимента |
| timestamp_start | DATETIME | Время начала run’а |
| timestamp_end | DATETIME | Время окончания run’а |
| tags | JSON | Теги эксперимента |

**Связи:**  
- One-to-Many: parameters, metrics, artifacts  
- One-to-One: dataset, code, environment

---

### 2. Parameter
| Поле | Тип | Описание |
|------|-----|----------|
| id | INTEGER PK | Уникальный |
| run_id | FK → Run.id | Run к которому относится параметр |
| key | STRING | Название параметра |
| value | STRING | Значение параметра (строка) |

---

### 3. Metric
| Поле | Тип | Описание |
|------|-----|----------|
| id | INTEGER PK | Уникальный |
| run_id | FK → Run.id | Run к которому относится метрика |
| key | STRING | Название метрики |
| value | FLOAT | Значение |
| step | INTEGER (опционально) | Шаг обучения |

---

### 4. Dataset
| Поле | Тип | Описание |
|------|-----|----------|
| id | INTEGER PK | Уникальный |
| run_id | FK → Run.id | Run |
| name | STRING | Название датасета |
| path | STRING | Путь к файлу |
| num_rows | INTEGER | Количество строк |
| num_columns | INTEGER | Количество столбцов |
| schema | JSON | Типы колонок |
| hash | STRING | SHA256 |

---

### 5. Code
| Поле | Тип | Описание |
|------|-----|----------|
| id | INTEGER PK | Уникальный |
| run_id | FK → Run.id | Run |
| git_commit | STRING | SHA коммита |
| entrypoint | STRING | Точка входа |
| tracked_files | JSON | Список файлов с хэшами |

---

### 6. Environment
| Поле | Тип | Описание |
|------|-----|----------|
| id | INTEGER PK | Уникальный |
| run_id | FK → Run.id | Run |
| python_version | STRING | Версия Python |
| pip_freeze | JSON | Список пакетов с версиями |
| os | STRING | Операционная система |

---

### 7. Artifact
| Поле | Тип | Описание |
|------|-----|----------|
| id | INTEGER PK | Уникальный |
| run_id | FK → Run.id | Run |
| name | STRING | Название артефакта |
| type | STRING | Тип (модель, график, лог) |
| path | STRING | Путь к файлу |

---

## Связи
- Run 1→M Parameter  
- Run 1→M Metric  
- Run 1→M Artifact  
- Run 1→1 Dataset  
- Run 1→1 Code  
- Run 1→1 Environment

