from flask import Blueprint, abort
from apifairy import authenticate, response, body, other_responses

from src.extensions import db
from src.auth import token_auth
from src.models import Task, Project
from src.schemas import TaskSchema, EmptySchema


tasks = Blueprint('tasks', __name__)

task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)
update_task_schema = TaskSchema(partial=True)


@tasks.route('/Tasks', methods=['POST'])
@authenticate(token_auth)
@body(task_schema)
@response(task_schema, 201)
@other_responses({404: 'Project not found', 401: 'User not allowed'})
def new_task(args, project_id):
    """Create a new Task"""
    user = token_auth.current_user()
    project = db.session.get(Project, project_id) or abort(404)
    if not project.user_id == user.id:
        abort(401)
    task = Task(project=project, **args)
    db.session.add(task)
    db.session.commit()
    return task


@tasks.route('/tasks', methods=['GET'])
@authenticate(token_auth)
@response(tasks_schema)
@other_responses({404: 'Project not found', 401: 'User not allowed'})
def get_tasks(project_id):
    """Return all Tasks"""
    user = token_auth.current_user()
    project = db.session.get(Project, project_id) or abort(404)
    if not project.user_id == user.id:
        abort(401)
    return project.tasks


@tasks.route('/Tasks/<int:Task_id>', methods=['GET'])
@authenticate(token_auth)
@response(task_schema)
@other_responses({404: 'Project or Task not found', 401: 'User not allowed'})
def get_task(project_id, task_id):
    """Return a Task by id"""
    user = token_auth.current_user()
    project = db.session.get(Project, project_id) or abort(404)
    if not project.user_id == user.id:
        abort(401)
    return db.session.get(Task, task_id) or abort(404)


@tasks.route('/Tasks/<int:Task_id>', methods=['PUT'])
@authenticate(token_auth)
@body(update_task_schema)
@response(task_schema)
@other_responses({404: 'Project or Task not found', 401: 'User not allowed'})
def update_task(data, project_id, task_id):
    """Update Task data"""
    user = token_auth.current_user()
    project = db.session.get(Project, project_id) or abort(404)
    if not project.user_id == user.id:
        abort(401)
    task = db.session.get(Task, task_id) or abort(404)
    task.update(data)
    db.session.add(task)
    db.session.commit()
    return task


@tasks.route('/Tasks/<int:Task_id>', methods=['DELETE'])
@authenticate(token_auth)
@response(EmptySchema, 204, description='Task deleted')
@other_responses({404: 'Project or Product not found', 401: 'User not allowed'})
def delete_task(project_id, task_id):
    """Delete a Task by id"""
    user = token_auth.current_user()
    project = db.session.get(Project, project_id) or abort(404)
    if not project.user_id == user.id:
        abort(401)
    task = db.session.get(Task, task_id) or abort(404)
    db.session.delete(task)
    db.session.commit()
    return {}
