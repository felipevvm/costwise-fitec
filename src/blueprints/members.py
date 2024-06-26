from flask import Blueprint, abort
from apifairy import authenticate, response, body, other_responses

from src.extensions import db
from src.auth import token_auth
from src.models import Member, Task, Project
from src.schemas import MemberSchema, EmptySchema

members = Blueprint('members', __name__)

member_schema = MemberSchema()
members_schema = MemberSchema(many=True)
update_member_schema = MemberSchema(partial=True)


@members.route('/members', methods=['GET'])
@authenticate(token_auth)
@response(members_schema, 200)
@other_responses({404: 'Project not found', 401: 'User not allowed'})
def get_members(project_id):
    """Return all Members"""
    user = token_auth.current_user()
    project = db.session.get(Project, project_id) or abort(404)
    if not project.user_id == user.id:
        abort(401)
    return project.members


@members.route('/members', methods=['POST'])
@authenticate(token_auth)
@body(member_schema)
@response(member_schema, 201)
@other_responses({404: 'Project not found', 401: 'User not allowed'})
def new_members(args, project_id):
    """Create a new Member"""
    user = token_auth.current_user()
    project = db.session.get(Project, project_id) or abort(404)
    if not project.user_id == user.id:
        abort(401)
    member = Member(project=project, **args)
    db.session.add(member)
    db.session.commit()
    project.update_budget()
    return member


@members.route('/members/<int:member_id>', methods=['GET'])
@authenticate(token_auth)
@response(member_schema)
@other_responses({404: 'Project or Member not found', 401: 'User not allowed'})
def get_member(project_id, member_id):
    """Return a Member by id"""
    user = token_auth.current_user()
    project = db.session.get(Project, project_id) or abort(404)
    if not project.user_id == user.id:
        abort(401)
    return db.session.get(Member, member_id) or abort(404)


@members.route('/members/<int:member_id>', methods=['PUT'])
@authenticate(token_auth)
@body(update_member_schema)
@response(member_schema)
@other_responses({404: 'Project or Member not found', 401: 'User not allowed'})
def update_member(data, project_id, member_id):
    """Update Member data"""
    user = token_auth.current_user()
    project = db.session.get(Project, project_id) or abort(404)
    if not project.user_id == user.id:
        abort(401)
    member = db.session.get(Member, member_id) or abort(404)
    member.update(data)
    db.session.add(member)
    db.session.commit()
    project.update_budget()
    return member


@members.route('/members/<int:member_id>', methods=['DELETE'])
@authenticate(token_auth)
@response(EmptySchema, 204, description='Member deleted')
@other_responses({404: 'Project or Member not found', 401: 'User not allowed'})
def delete_member(project_id, member_id):
    """Delete a Member by id"""
    user = token_auth.current_user()
    project = db.session.get(Project, project_id) or abort(404)
    if not project.user_id == user.id:
        abort(401)
    member = db.session.get(Member, member_id) or abort(404)
    db.session.delete(member)
    db.session.commit()
    project.update_budget()
    return {}


@members.route('/members/<int:member_id>/<int:task_id>', methods=['PUT'])
@authenticate(token_auth)
@response(member_schema)
@other_responses({404: 'Project or Member or Task not found', 401: 'User not allowed',
                  409: 'Task already assigned.'})
def assign_task(project_id, member_id, task_id):
    """Assign a Task to a Member"""
    user = token_auth.current_user()
    project = db.session.get(Project, project_id) or abort(404)
    if not project.user_id == user.id:
        abort(401)
    member = db.session.get(Member, member_id) or abort(404)
    task = db.session.get(Task, task_id) or abort(404)
    if member.has_task(task):
        abort(409)
    member.assign_task(task)
    db.session.commit()
    project.update_budget()
    return member
