# Todo API — Interview Project

A small REST API for managing a todo list, built with Python & Flask.

## Getting Started

```bash
# 1. Clone the repo
git clone <repo-url>
cd python-todo-interview

# 2. Create a virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the server
python app.py
```

Server runs at `http://localhost:5000`

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/todos` | List all todos (optional: `?completed=true/false`) |
| POST | `/todos` | Create a todo (`title`, `priority`: low/medium/high) |
| GET | `/todos/<id>` | Get a todo by ID |
| PUT | `/todos/<id>` | Update a todo |
| DELETE | `/todos/<id>` | Delete a todo |
| GET | `/todos/stats` | Get summary statistics |

## Running Tests

```bash
pytest tests/ -v
```

## Your Tasks

1. **Fork** this repo and create a branch called `interview/<your-name>`
2. **Run the tests** — some will fail. Find and fix the bugs causing them.
3. **Add a new feature:** implement a `PATCH /todos/<id>/complete` endpoint that marks a todo as completed (shortcut instead of using PUT).
4. **Commit your changes** with clear commit messages and open a **Pull Request** back to the main branch.
