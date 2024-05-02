from flask import Blueprint, abort
from apifairy import response, body, other_responses

from .models import Task, db
from .schemas import TaskSchema, EmptySchema

tasks = Blueprint('tasks', __name__)

task_schema = TaskSchema()
update_task_schema = TaskSchema(partial=True)
tasks_schema = TaskSchema(many=True)


@tasks.route('/tasks', methods=['GET'])
@response(tasks_schema)
def all_tasks():
    """Shows all Tasks"""
    return Task.query.all()


@tasks.route('/Tasks', methods=['POST'])
@body(task_schema)
@response(task_schema, 201)
def new_Task(args):
    """Create a new Task"""
    Task = Task(**args)
    db.session.add(Task)
    db.session.commit()
    return Task


@tasks.route('/Tasks/<int:Task_id>', methods=['GET'])
@response(Task_schema)
@other_responses({404: 'Task not found'})
def get_Task(Task_id):
    """Return a Task by id"""
    return db.session.get(Task, Task_id) or abort(404)


@Tasks.route('/Tasks/<int:Task_id>', methods=['PUT'])
@body(update_Task_schema)
@response(Task_schema)
@other_responses({404: 'Task not found'})
def update_Task(data, Task_id):
    """Update Task data"""
    Task = db.session.get(Task, Task_id) or abort(404)
    Task.update(data)
    db.session.commit()
    return Task


@tasks.route('/Tasks/<int:Task_id>', methods=['DELETE'])
@response(EmptySchema, 204, description='Task deleted')
@other_responses({404: 'Task not found'})
def delete_Task(Task_id):
    """Delete a Task by id"""
    Task = db.session.get(Task, Task_id) or abort(404)
    db.session.delete(Task)
    db.session.commit()
    return {}
