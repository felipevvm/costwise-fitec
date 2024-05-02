from flask import Blueprint, abort
from apifairy import authenticate, response, body, other_responses

from src.extensions import db
from src.auth import token_auth
from src.models import Project
from src.schemas import ProjectSchema, EmptySchema

projects = Blueprint('projects', __name__)

project_schema = ProjectSchema()
projects_schema = ProjectSchema(many=True)
update_project_schema = ProjectSchema(partial=True)


@projects.route('/projects', methods=['POST'])
@authenticate(token_auth)
@body(project_schema)
@response(project_schema)
def new_project(args):
    """Create a new Project"""
    user = token_auth.current_user()
    project = Project(owner=user, **args)
    db.session.add(project)
    db.session.commit()
    return project


@projects.route('/projects', methods=['GET'])
@authenticate(token_auth)
@response(projects_schema)
def get_projects():
    """Return all user Projects"""
    user = token_auth.current_user()
    return Project.query.where(Project.user_id == user.id).all()


@projects.route('/projects/<int:project_id>', methods=['GET'])
@authenticate(token_auth)
@response(project_schema)
@other_responses({404: 'Project Not found', 401: 'User not allow to view this project'})
def get_project(project_id):
    """Return a Project by id"""
    user = token_auth.current_user()
    project = db.session.get(Project, project_id) or abort(404)
    if project.user_id == user.id:
        return project
    abort(401)


@projects.route('/projects/<int:project_id>', methods=['PUT'])
@authenticate(token_auth)
@body(update_project_schema)
@response(project_schema)
@other_responses({404: 'Project Not found', 401: 'User not allow to edit this project'})
def update_project(data, project_id):
    """Update Project data"""
    user = token_auth.current_user()
    project = db.session.get(Project, project_id) or abort(404)
    if project.user_id == user.id:
        project.update(data)
        db.session.commit()
        return project
    abort(401)


@projects.route('/projects/<int:project_id>', methods=['DELETE'])
@authenticate(token_auth)
@response(EmptySchema)
@other_responses({404: 'Project Not found', 401: 'User not allow to delete this project'})
def delete_project(project_id):
    """Delete a Project by id"""
    user = token_auth.current_user()
    project = db.session.get(Project, project_id) or abort(404)
    if project.user_id == user.id:
        db.session.delete(project)
        db.session.commit()
        return {}
    abort(401)
