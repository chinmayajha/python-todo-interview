import pytest
from app import app, todos


@pytest.fixture(autouse=True)
def clear_todos():
    """Reset todos before each test."""
    todos.clear()
    yield
    todos.clear()


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_get_todos_empty(client):
    res = client.get("/todos")
    assert res.status_code == 200
    assert res.json["todos"] == []
    assert res.json["count"] == 0


def test_create_todo(client):
    res = client.post("/todos", json={"title": "Buy milk"})
    assert res.status_code == 201
    assert res.json["title"] == "Buy milk"
    assert res.json["completed"] is False
    assert res.json["priority"] == "medium"


def test_create_todo_missing_title(client):
    res = client.post("/todos", json={})
    assert res.status_code == 400


def test_create_todo_low_priority(client):
    res = client.post("/todos", json={"title": "Task", "priority": "low"})
    assert res.status_code == 201  # Fails until Bug 2 is fixed


def test_get_todo_by_id(client):
    create = client.post("/todos", json={"title": "Test task"})
    todo_id = create.json["id"]
    res = client.get(f"/todos/{todo_id}")
    assert res.status_code == 200
    assert res.json["id"] == todo_id


def test_update_todo(client):
    create = client.post("/todos", json={"title": "Old title"})
    todo_id = create.json["id"]
    res = client.put(f"/todos/{todo_id}", json={"title": "New title", "completed": True})
    assert res.status_code == 200
    assert res.json["title"] == "New title"
    assert res.json["completed"] is True


def test_delete_todo(client):
    create = client.post("/todos", json={"title": "Delete me"})
    todo_id = create.json["id"]
    res = client.delete(f"/todos/{todo_id}")
    assert res.status_code == 200  # Fails until Bug 3 is fixed


def test_filter_completed_todos(client):
    client.post("/todos", json={"title": "Task A"})
    create = client.post("/todos", json={"title": "Task B"})
    todo_id = create.json["id"]
    client.put(f"/todos/{todo_id}", json={"completed": True})

    res = client.get("/todos?completed=true")
    assert res.status_code == 200
    assert all(t["completed"] is True for t in res.json["todos"])  # Fails until Bug 1 is fixed


def test_stats(client):
    client.post("/todos", json={"title": "Task 1", "priority": "medium"})
    client.post("/todos", json={"title": "Task 2", "priority": "high"})
    res = client.get("/todos/stats")
    assert res.status_code == 200
    assert res.json["total"] == 2
    assert res.json["pending"] == 2
