import enum

from flask import url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class Updateable:
    def update(self, data):
        for attr, value in data.items():
            setattr(self, attr, value)


user_project = db.Table('user_project',
                        db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
                        db.Column('project_id', db.Integer, db.ForeignKey('project.id'), primary_key=True))


class User(Updateable, db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False, unique=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password_hash = db.Column(db.String(255))

    @property
    def url(self):
        return url_for('users.get_user', id=self.id)

    def __repr__(self):
        return '<User {}-{}>'.format(self.id, self.username)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


class Project(db.Model):
    __tablename__ = "project"

    id = db.Column(db.Integer, primary_key=True)
    name_project = db.Column(db.String(255), nullable=False)
    deadline = db.Column(db.Date)
    budget = db.Column(db.Integer)
    total_cost_software = db.Column(db.Integer)
    total_cost_hardware = db.Column(db.Integer)
    total_cost_other = db.Column(db.Integer)
    total_time_tasks = db.Column(db.DateTime)

    members = db.relationship('Member', backref='project')
    tasks = db.relationship('Task', backref='project')
    products = db.relationship('Product', backref='project')
    users = db.relationship('User', secondary=user_project, backref='projects')


member_task = db.Table('member_task',
                       db.Column('member_id', db.Integer, db.ForeignKey('member.id'), primary_key=True),
                       db.Column('task_id', db.Integer, db.ForeignKey('task.id'), primary_key=True))


class Member(db.Model):
    __tablename__ = "member"

    id = db.Column(db.Integer, primary_key=True)
    name_member = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(255), nullable=False)
    salary = db.Column(db.Integer)

    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)


class Task(db.Model):
    __tablename__ = "task"

    id = db.Column(db.Integer, primary_key=True)
    name_task = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(500))
    deadline = db.Column(db.Date)

    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    members = db.relationship('Member', secondary=member_task, backref='tasks')


class ProductType(enum.Enum):
    HARDWARE = 'Hardware'
    SOFTWARE = 'Software'
    OTHER = 'Other'


class Product(db.Model):
    __tablename__ = "product"

    id = db.Column(db.Integer, primary_key=True)
    name_product = db.Column(db.String(255), nullable=False)
    cost = db.Column(db.Integer, nullable=False)
    license = db.Column(db.Boolean, nullable=False)
    type = db.Column(db.Enum(ProductType))
    amount = db.Column(db.Integer)

    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
