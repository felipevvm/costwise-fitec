from flask import Blueprint
from flask import Blueprint, abort, jsonify
from apifairy import APIFairy
from apifairy import response, body, other_responses

from .models import Member, db, Updateable
from .schemas import MemberSchema, EmptySchema

members = Blueprint('members', __name__)

member_schema = MemberSchema()
update_member_schema = MemberSchema(partial=True)
Members_schema = MemberSchema(many=True)

@members.route('/members', methods=['POST'])
@body(members_schema)
@response(members_schema, 201)
def new_members(args):
    member = Members(**args)
    db.session.add(member)
    db.session.commit()
    return member

@members.route('/members', methods=['GET'])
@response(members_schema)
def all_members():
    return member.query.all()

@members.route('/members/<int:member_id>', methods=['GET'])
@response(member_schema)
@other_responses({404: 'User not found'})
def get_member(members_id):
    return db.session.get(Member, member_id) or abort(404)

@members.route('/members/<string:member_id>', methods=['GET'])
@response(member_schema)
@other_responses({404:'User not found'})
def get_member(members_id_project):
    return db.session.get(Member, members_id_project) or abort (404)

@members.route('/members/<int:member_id>', methods=['DELETE'])
@response(EmptySchema, 204, description='Member deleted')
@other_responses({404: 'User not found'})
def delete_member(members_id):
    member = db.session.get(Member, member_id) or abort(404)
    db.session.delete(member)
    db.session.commit()
    return {}


