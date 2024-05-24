from flask import Blueprint, abort
from apifairy import authenticate, response, body, other_responses

from src.extensions import db
from src.auth import token_auth
from src.models import Project,  Member, Product
from src.schemas import ProjectSchema, CostProductLicenseSchema, CostProductTypeSchema, CostMembersSchema, EmptySchema
from .products import products
from .members import members
from .tasks import tasks

projects = Blueprint('projects', __name__)

projects.register_blueprint(products, url_prefix='projects/<int:project_id>')
projects.register_blueprint(members, url_prefix='projects/<int:project_id>')
projects.register_blueprint(tasks, url_prefix='projects/<int:project_id>')

project_schema = ProjectSchema()
projects_schema = ProjectSchema(many=True)
update_project_schema = ProjectSchema(partial=True)
cost_products_by_license = CostProductLicenseSchema()
cost_products_by_type = CostProductTypeSchema()
cost_members = CostMembersSchema()


@projects.route('/projects', methods=['GET'])
@authenticate(token_auth)
@response(projects_schema)
def get_projects():
    """Return all user Projects"""
    user = token_auth.current_user()
    return Project.query.where(Project.user_id == user.id).all()


@projects.route('/projects', methods=['POST'])
@authenticate(token_auth)
@body(project_schema)
@response(project_schema, 201)
def new_project(args):
    """Create a new Project"""
    user = token_auth.current_user()
    project = Project(owner=user, **args)
    db.session.add(project)
    db.session.commit()
    return project


@projects.route('/projects/<int:project_id>', methods=['GET'])
@authenticate(token_auth)
@response(project_schema)
@other_responses({404: 'Project not found', 401: 'User not allow to view this project'})
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
@other_responses({404: 'Project not found', 401: 'User not allow to edit this project'})
def update_project(data, project_id):
    """Update Project data"""
    user = token_auth.current_user()
    project = db.session.get(Project, project_id) or abort(404)
    if not project.user_id == user.id:
        abort(401)
    project.update(data)
    db.session.commit()
    project.update_budget()
    return project


@projects.route('/projects/<int:project_id>', methods=['DELETE'])
@authenticate(token_auth)
@response(EmptySchema, 204, description='Project deleted')
@other_responses({404: 'Project not found', 401: 'User not allow to delete this project'})
def delete_project(project_id):
    """Delete a Project by id"""
    user = token_auth.current_user()
    project = db.session.get(Project, project_id) or abort(404)
    if not project.user_id == user.id:
        abort(401)
    db.session.delete(project)
    db.session.commit()
    return {}


@projects.route('projects/<int:project_id>/members_costs', methods=['GET'])
@authenticate(token_auth)
@response(cost_members)
@other_responses({404: 'Project not found', 401: 'User not allowed'})
def get_cost_of_all_members(project_id):
    """Return the total cost of all members"""
    user = token_auth.current_user()
    project = db.session.get(Project, project_id) or abort(404)
    if not project.user_id == user.id:
        abort(401)
    return {'Members': Member.calc_costs_for_all_members(project_id)}


@projects.route('projects/<int:project_id>/products_by_license', methods=['GET'])
@authenticate(token_auth)
@response(cost_products_by_license)
@other_responses({404: 'Project not found', 401: 'User not allowed'})
def get_cost_of_all_products_by_license(project_id):
    """Return the total cost of all products by license"""
    user = token_auth.current_user()
    project = db.session.get(Project, project_id) or abort(404)
    if not project.user_id == user.id:
        abort(401)
    return Product.calc_total_costs_by_license(project_id)


@projects.route('projects/<int:project_id>/products_by_type', methods=['GET'])
@authenticate(token_auth)
@response(cost_products_by_type)
@other_responses({404: 'Project not found', 401: 'User not allowed'})
def get_cost_of_all_products_by_type(project_id):
    """Return the total cost of all products by type"""
    user = token_auth.current_user()
    project = db.session.get(Project, project_id) or abort(404)
    if not project.user_id == user.id:
        abort(401)
    return Product.calc_total_costs_by_type(project_id)
