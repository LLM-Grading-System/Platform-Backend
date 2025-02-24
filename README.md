## Документация

### Модель данных
```mermaid
erDiagram
    User {
        UUID user_id PK
        string login
        string salt
        string hashed_password
        string role
        datetime created_at
    }

    Session {
        UUID session_id PK
        UUID user_id FK
        datetime expired_at
        string user_agent
    }

    Student {
        UUID student_id PK
        int tg_user_id
        string tg_username
        string gh_username
        datetime registered_at
    }

    Task {
        UUID task_id PK
        string name
        string description
        string gh_repo_url
        string level
        string tags
        bool is_draft
    }

    Criteria {
        UUID criteria_id PK
        UUID task_id FK
        string description
        float weight
        datetime created_at
    }

    Attempt {
        UUID attempt_id PK
        UUID task_id FK
        UUID student_id FK
        string gh_repo_url
        float llm_grade
        string llm_feedback
        float teacher_grade
        string teacher_feedback
        datetime created_at
        datetime evaluated_at
    }

    CriteriaFeedback {
        UUID criteria_feedback_id PK
        UUID attempt_id FK
        UUID criteria_id FK
        bool is_confirmed
        string llm_feedback
    }

    %% Relationships
    User ||--o{ Session : has
    Student ||--o{ Attempt : makes
    Task ||--o{ Criteria : has
    Task ||--o{ Attempt : has
    Attempt ||--o{ CriteriaFeedback : has
    Criteria ||--o{ CriteriaFeedback : has
```

## Разработка

### Установка библиотек с uv
```bash
uv sync
```

### Запуск контейнеров для разработки
```bash
docker compose -f dev.docker-compose.yaml up -d
```

### Запуск в dev-режиме
```bash
uv run fastapi dev src/app.py
```

### Запуск форматтера и линтера с автофиксами
```bash
uv run ruff format ./src
uv run ruff check --fix src
```

### Запуск в production-режиме
```bash
uv run granian --interface asgi src.app:app
```