from datetime import date

from marshmallow import validate

from .extensions import ma
from .models import User, Project, Member, Task, Product, ProductType


class EmptySchema(ma.Schema):
    pass


# noinspection PyUnresolvedReferences
class TokenSchema(ma.Schema):
    class Meta:
        ordered = True

    access_token = ma.String(required=True)
    refresh_token = ma.String()


class AllUsersSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User
        include_fk = True
        include_relationships = True
        ordered = True

    id = ma.auto_field(dump_only=True)
    email = ma.Email(required=True, validate=validate.And(validate.Email(),
                                                          validate.Length(min=5, max=255))
                     )
    username = ma.auto_field(required=True, validate=validate.Length(min=5, max=255))


# noinspection PyUnresolvedReferences
class UserSchema(AllUsersSchema, ma.SQLAlchemySchema):
    class Meta:
        model = User
        include_fk = True
        include_relationships = True
        ordered = True

    password = ma.String(required=True, load_only=True, validate=validate.Length(min=5, max=255))
    projects = ma.Nested(lambda: ProjectSchema(only=['id', 'name_project']), many=True, dump_only=True)


class ProjectSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Project
        include_fk = True
        include_relationships = True
        ordered = True

    id = ma.auto_field(dump_only=True)
    name_project = ma.auto_field(required=True, validate=validate.Length(min=1, max=255))
    description_project = ma.auto_field(validate=validate.Length(max=500))
    deadline = ma.auto_field(required=True, validate=validate.Range(min=date.today()))
    created_at = ma.auto_field(dump_only=True)
    budget = ma.auto_field(dump_only=True)
    expected_budget = ma.Number(validate=validate.Range(min=0))
    total_cost_products = ma.auto_field(dump_only=True)
    total_cost_members = ma.auto_field(dump_only=True)

    owner = ma.Nested(UserSchema(only=['username', 'email']), dump_only=True)
    user_id = ma.auto_field(dump_only=True)
    members = ma.Nested(lambda: MemberSchema(only=['id', 'name_member']), many=True, dump_only=True)
    products = ma.Nested(lambda: ProductSchema(only=['id', 'name_product']), many=True, dump_only=True)
    tasks = ma.Nested(lambda: TaskSchema(only=['id', 'name_task']), many=True, dump_only=True)


class MemberSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Member
        include_fk = True
        include_relationships = True

    id = ma.auto_field(dump_only=True)
    name_member = ma.auto_field(required=True, validate=validate.Length(min=1, max=255))
    role = ma.auto_field(required=True, validate=validate.Length(min=5, max=255))
    salary = ma.auto_field(required=True, validate=validate.Range(min=0))

    project_id = ma.auto_field(dump_only=True)
    project = ma.Nested(ProjectSchema(only=['name_project', 'user_id']), dump_only=True)
    tasks = ma.Nested(lambda: TaskSchema(only=['id', 'name_task']), many=True, dump_only=True)


class TaskSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Task
        include_fk = True
        include_relationships = True

    id = ma.auto_field(dump_only=True)
    name_task = ma.auto_field(required=True, validate=validate.Length(min=1, max=255))
    description_task = ma.auto_field(validate=validate.Length(max=500))
    deadline = ma.auto_field(required=True, validate=validate.Range(min=date.today()))
    created_at = ma.auto_field(dump_only=True)

    project_id = ma.auto_field(dump_only=True)
    project = ma.Nested(ProjectSchema(only=['name_project', 'user_id']), dump_only=True)
    members = ma.Nested(MemberSchema(only=['id', 'name_member', 'role']), many=True, dump_only=True)


class ProductSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Product
        include_fk = True
        include_relationships = True

    id = ma.auto_field(dump_only=True)
    name_product = ma.auto_field(required=True, validate=validate.Length(min=1, max=255))
    description_product = ma.auto_field(validate=validate.Length(max=500))
    type = ma.Enum(ProductType, required=True)
    license = ma.Boolean(required=True)
    cost = ma.auto_field(required=True, validate=validate.Range(min=0))
    amount = ma.auto_field(required=True, validate=validate.Range(min=0))
    project_id = ma.auto_field(dump_only=True)
    project = ma.Nested(ProjectSchema, only=['name_project', 'user_id'], dump_only=True)


class MemberCostSchema(ma.Schema):
    member = ma.String()
    total_cost = ma.Number()


class CostMembersSchema(ma.Schema):
    Members = ma.Nested(MemberCostSchema, many=True)


class CostProductLicenseSchema(ma.Schema):
    license_cost = ma.Number()
    no_license_cost = ma.Number()


class CostProductTypeSchema(ma.Schema):
    HARDWARE = ma.Number()
    SOFTWARE = ma.Number()
    OTHER = ma.Number()


class PasswordResetRequestSchema(ma.Schema):
    class Meta:
        ordered = True

    email = ma.String(required=True, validate=validate.Email())


class PasswordResetSchema(ma.Schema):
    class Meta:
        ordered = True

    token = ma.String(required=True)
    new_password = ma.String(required=True, validate=validate.Length(min=3))
