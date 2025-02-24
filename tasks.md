## Задачи по проекту

☑️ 🔄 🟦

### REST API

#### Схемы
- CreateUpdateTask: {name: string, description: string, gh_repo_url: string, level: string, is_draft: bool, tags: Array<string>}
- FullTask: {task_id: string, name: string, description: string, gh_repo_url: string, level: string, is_draft: bool, created_at: timestamp, tags: Array<string>}
- ShortTask: {task_id: string, name: string, level: string, is_draft: bool, created_at: timestamp, tags: Array<string>}
- CreateUpdateCriteria: {description: string, weight: number}
- Criteria: {criteria_id: string, description: string, weight: number, created_at: timestamp}
- CreateSolution: {gh_repo_url: string}
- Solution: {solution_id: string, task_id: string, student_id: string, status: string, gh_repo_url: string}
- CriteriaFeedback: {criteria_id: string, llm_grade: number, llm_feedback: string}
- AttemptFeedback: {llm_grade: number, llm_feedback: string, criteria_feedbacks: Array<CriteriaFeedback>}
- Attempt: {attempt_id: string, solution_id: string, llm_grade: number, llm_feedback: string, created_at: timestamp, evaluated_at: timestamp, criteria: Array<CriteriaFeedback>}

#### Работа с пользователями

- Вход на платформу
  - POST /api/auth/login
  - Request: {login: string, password: string}
  - Response: {token: string}


#### Работа с задачами

- Создание задачи
  - POST /api/tasks
  - Request: CreateUpdateTask
  - Response: FullTask
- Получение всех задач
  - GET /api/tasks?github_url=...
  - Response: Array<ShortTask>
- Получение полной информации о задачи:
  - GET /api/tasks/:task_id
  - Response: FullTask
- Редактирование задачи
  - PUT /api/tasks/:task_id
  - Request: CreateUpdateTask
  - Response: FullTask
- Удаление задачи
  - DELETE /api/tasks/:task_id
  - Response: {"message": "Задача удалена"}
- Получение критериев задачи
  - GET /api/tasks/:task_id/criteria
  - Response: Array<Criteria>
- Создание нового критерия для задачи
  - POST /api/tasks/:task_id/criteria
  - Request: CreateUpdateCriteria
  - Response: Criteria
- Редактирование критерия для задачи
  - PUT /api/tasks/:task_id/criteria
  - Request: CreateUpdateCriteria
  - Response: Criteria
- Удаление критерия задачи
  - DELETE /api/tasks/:task_id/criteria/:criteria_id
  - Response: {"message": "Критерий удален"}

#### Работа с решениями студентов

- Регистрация попытки студента
  - POST /api/solutions
  - Request: CreateSolution
  - Response: {"message": "Заявка на проверку создана"}
- Получение решений
  - GET /api/solutions?task_id=...
  - Response: Array<Solution>
- Добавление фидбека по попытке решения
  - POST /api/solutions/:solution_id/attempts/:attempt_id
  - Request: AttemptFeedback
  - Response: {"message": "Фидбек добавлен"}
- Получение решения
  - GET /api/solutions/:solution_id
  - Response: Solution
- Получение попыток решения
  - GET /api/solutions/:solution_id
  - Response: Array<Attempt>

