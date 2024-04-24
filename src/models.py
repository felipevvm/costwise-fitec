import enum

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


user_project = db.Table('user_project',
                        db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
                        db.Column('project_id', db.Integer, db.ForeignKey('project.id'), primary_key=True))


class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False, unique=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)

    projects = db.relationship('project', secondary=user_project, backref='users')


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

    members = db.relationship('member', backref='project')
    tasks = db.relationship('task', backref='project')
    products = db.relationship('product', backref='project')


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
