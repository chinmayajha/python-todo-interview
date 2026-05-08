from flask import Flask, jsonify, request
from datetime import datetime
import uuid

app = Flask(__name__)

# In-memory "database"
todos = {}


def create_todo(title, priority="medium"):
    """Create a new todo item."""
    todo_id = str(uuid.uuid4())
    todo = {
        "id": todo_id,
        "title": title,
        "completed": False,
        "priority": priority,
        "created_at": datetime.utcnow().isoformat(),
    }
    todos[todo_id] = todo
    return todo


# BUG 1 — Logic (filter is inverted)
# Uses `!=` instead of `==`, so ?completed=true returns incomplete todos.
def filter_todos(completed=None):
    if completed is None:
        return list(todos.values())
    return [todo for todo in todos.values() if todo["completed"] != completed]


# BUG 2 — Missing value in validation list
# "low" is missing from VALID_PRIORITIES, so setting priority="low" always 400s.
VALID_PRIORITIES = ["medium", "high"]


@app.route("/todos", methods=["GET"])
def get_todos():
    """Get all todos. Optional: ?completed=true|false"""
    completed_param = request.args.get("completed")
    if completed_param is not None:
        if completed_param.lower() not in ("true", "false"):
            return jsonify({"error": "completed must be 'true' or 'false'"}), 400
        filter_completed = completed_param.lower() == "true"
        result = filter_todos(completed=filter_completed)
    else:
        result = filter_todos()
    return jsonify({"todos": result, "count": len(result)}), 200


@app.route("/todos", methods=["POST"])
def add_todo():
    """Create a new todo. Body: { "title": "...", "priority": "low|medium|high" }"""
    data = request.get_json()
    if not data or "title" not in data:
        return jsonify({"error": "title is required"}), 400
    title = data["title"].strip()
    if not title:
        return jsonify({"error": "title cannot be empty"}), 400
    priority = data.get("priority", "medium")
    if priority not in VALID_PRIORITIES:
        return jsonify({"error": f"priority must be one of {VALID_PRIORITIES}"}), 400
    todo = create_todo(title, priority)
    return jsonify(todo), 201


@app.route("/todos/<todo_id>", methods=["GET"])
def get_todo(todo_id):
    """Get a single todo by ID."""
    todo = todos.get(todo_id)
    if not todo:
        return jsonify({"error": "Todo not found"}), 404
    return jsonify(todo), 200


@app.route("/todos/<todo_id>", methods=["PUT"])
def update_todo(todo_id):
    """Update a todo's title, priority, or completed status."""
    todo = todos.get(todo_id)
    if not todo:
        return jsonify({"error": "Todo not found"}), 404
    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body required"}), 400
    if "title" in data:
        title = data["title"].strip()
        if not title:
            return jsonify({"error": "title cannot be empty"}), 400
        todo["title"] = title
    if "priority" in data:
        if data["priority"] not in VALID_PRIORITIES:
            return jsonify({"error": f"priority must be one of {VALID_PRIORITIES}"}), 400
        todo["priority"] = data["priority"]
    if "completed" in data:
        if not isinstance(data["completed"], bool):
            return jsonify({"error": "completed must be a boolean"}), 400
        todo["completed"] = data["completed"]
    return jsonify(todo), 200


# BUG 3 — Wrong HTTP status code
# Returns 201 (Created) on DELETE. Should be 200 (OK).
@app.route("/todos/<todo_id>", methods=["DELETE"])
def delete_todo(todo_id):
    """Delete a todo by ID."""
    todo = todos.get(todo_id)
    if not todo:
        return jsonify({"error": "Todo not found"}), 404
    del todos[todo_id]
    return jsonify({"message": "Todo deleted successfully"}), 201  # BUG: should be 200


@app.route("/todos/stats", methods=["GET"])
def get_stats():
    """Return statistics about the todo list."""
    all_todos = list(todos.values())
    total = len(all_todos)
    completed = sum(1 for t in all_todos if t["completed"])
    pending = total - completed
    by_priority = {"low": 0, "medium": 0, "high": 0}
    for t in all_todos:
        by_priority[t["priority"]] += 1
    return jsonify({
        "total": total,
        "completed": completed,
        "pending": pending,
        "by_priority": by_priority,
    }), 200


if __name__ == "__main__":
    app.run(debug=True, port=5000)
