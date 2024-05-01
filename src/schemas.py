from flask_marshmallow import Marshmallow
from marshmallow_enum import EnumField

from .models import User, Project, Member, Task, Product, ProductType

ma = Marshmallow()


class EmptySchema(ma.Schema):
    pass


# noinspection PyUnresolvedReferences
class TokenSchema(ma.Schema):
    class Meta:
        ordered = True

    access_token = ma.String(required=True)
    refresh_token = ma.String()


# noinspection PyUnresolvedReferences
class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User
        include_fk = True
        include_relationships = True
        ordered = True

    id = ma.auto_field(dump_only=True)
    email = ma.auto_field(required=True)
    username = ma.auto_field(required=True)
    password = ma.String(required=True, load_only=True)
    projects = ma.auto_field(dump_only=True, load_only=True)


class ProjectSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Project
        include_fk = True
        include_relationships = True


class MemberSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Member
        include_fk = True
        include_relationships = True


class TaskSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Task
        include_fk = True
        include_relationships = True


class ProductSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Product
        include_fk = True
        include_relationships = True

    type = EnumField(ProductType)
