# coding: utf-8
from sqlalchemy import Column, Date, DateTime, ForeignKey, Index, Integer, SmallInteger, String, Table, Text
from sqlalchemy.orm import relationship
from sqlalchemy.schema import FetchedValue
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Complaint(db.Model):
    __tablename__ = 'Complaint'

    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.Text(collation='utf8_bin'), nullable=False)
    flat_id = db.Column(db.ForeignKey('Flat.id', onupdate='CASCADE'), nullable=False, index=True)
    comp_type_id = db.Column(db.ForeignKey('TypeComplaint.id', onupdate='CASCADE'), nullable=False, index=True)
    date = db.Column(db.Date, nullable=False)

    comp_type = db.relationship('TypeComplaint', primaryjoin='Complaint.comp_type_id == TypeComplaint.id', backref='complaints')
    flat = db.relationship('Flat', primaryjoin='Complaint.flat_id == Flat.id', backref='complaints')


class Flat(db.Model):
    __tablename__ = 'Flat'

    id = db.Column(db.Integer, primary_key=True)
    size = db.Column(db.Integer, nullable=False)
    owner_id = db.Column(db.ForeignKey('Owner.id', ondelete='SET NULL', onupdate='CASCADE'), index=True)
    house_id = db.Column(db.ForeignKey('House.id', ondelete='SET NULL', onupdate='CASCADE'), index=True)
    num = db.Column(db.Integer, nullable=False)

    house = db.relationship('House', primaryjoin='Flat.house_id == House.id', backref='flats')
    owner = db.relationship('Owner', primaryjoin='Flat.owner_id == Owner.id', backref='flats')


class House(db.Model):
    __tablename__ = 'House'

    id = db.Column(db.Integer, primary_key=True)
    adress = db.Column(db.String(200, 'utf8_bin'), nullable=False)
    photo = db.Column(db.String(200, 'utf8_bin'))
    name = db.Column(db.String(200, 'utf8_bin'), nullable=False)
    descr = db.Column(db.Text(collation='utf8_bin'), nullable=False)


class Owner(db.Model):
    __tablename__ = 'Owner'

    id = db.Column(db.Integer, primary_key=True)
    fio = db.Column(db.String(200, 'utf8_bin'), nullable=False)
    dob = db.Column(db.Date, nullable=False)


class Prof(db.Model):
    __tablename__ = 'Prof'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200, 'utf8_bin'), nullable=False)


class Request(db.Model):
    __tablename__ = 'Request'

    id = db.Column(db.Integer, primary_key=True)
    spec_id = db.Column(db.ForeignKey('Specialist.id', onupdate='CASCADE'), nullable=False, index=True)
    flat_id = db.Column(db.ForeignKey('Flat.id', onupdate='CASCADE'), nullable=False, index=True)
    date = db.Column(db.Date, nullable=False)
    comment = db.Column(db.Text(collation='utf8_bin'), nullable=False)

    flat = db.relationship('Flat', primaryjoin='Request.flat_id == Flat.id', backref='requests')
    spec = db.relationship('Specialist', primaryjoin='Request.spec_id == Specialist.id', backref='requests')


class Specialist(db.Model):
    __tablename__ = 'Specialist'

    id = db.Column(db.Integer, primary_key=True)
    fio = db.Column(db.String(200, 'utf8_bin'), nullable=False)
    experience = db.Column(db.Integer, nullable=False)
    prof_id = db.Column(db.ForeignKey('Prof.id', onupdate='CASCADE'), nullable=False, index=True)

    prof = db.relationship('Prof', primaryjoin='Specialist.prof_id == Prof.id', backref='specialists')


class TypeComplaint(db.Model):
    __tablename__ = 'TypeComplaint'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200, 'utf8_bin'), nullable=False)


class AuthGroup(db.Model):
    __tablename__ = 'auth_group'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)


class AuthGroupPermission(db.Model):
    __tablename__ = 'auth_group_permissions'
    __table_args__ = (
        db.Index('auth_group_permissions_group_id_permission_id_0cd325b0_uniq', 'group_id', 'permission_id'),
    )

    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.ForeignKey('auth_group.id'), nullable=False)
    permission_id = db.Column(db.ForeignKey('auth_permission.id'), nullable=False, index=True)

    group = db.relationship('AuthGroup', primaryjoin='AuthGroupPermission.group_id == AuthGroup.id', backref='auth_group_permissions')
    permission = db.relationship('AuthPermission', primaryjoin='AuthGroupPermission.permission_id == AuthPermission.id', backref='auth_group_permissions')


class AuthPermission(db.Model):
    __tablename__ = 'auth_permission'
    __table_args__ = (
        db.Index('auth_permission_content_type_id_codename_01ab375a_uniq', 'content_type_id', 'codename'),
    )

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    content_type_id = db.Column(db.ForeignKey('django_content_type.id'), nullable=False)
    codename = db.Column(db.String(100), nullable=False)

    content_type = db.relationship('DjangoContentType', primaryjoin='AuthPermission.content_type_id == DjangoContentType.id', backref='auth_permissions')


class AuthUser(db.Model):
    __tablename__ = 'auth_user'

    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(128), nullable=False)
    last_login = db.Column(db.DateTime)
    is_superuser = db.Column(db.Integer, nullable=False)
    username = db.Column(db.String(150), nullable=False, unique=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(254), nullable=False)
    is_staff = db.Column(db.Integer, nullable=False)
    is_active = db.Column(db.Integer, nullable=False)
    date_joined = db.Column(db.DateTime, nullable=False)


class AuthUserGroup(db.Model):
    __tablename__ = 'auth_user_groups'
    __table_args__ = (
        db.Index('auth_user_groups_user_id_group_id_94350c0c_uniq', 'user_id', 'group_id'),
    )

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.ForeignKey('auth_user.id'), nullable=False)
    group_id = db.Column(db.ForeignKey('auth_group.id'), nullable=False, index=True)

    group = db.relationship('AuthGroup', primaryjoin='AuthUserGroup.group_id == AuthGroup.id', backref='auth_user_groups')
    user = db.relationship('AuthUser', primaryjoin='AuthUserGroup.user_id == AuthUser.id', backref='auth_user_groups')


class AuthUserUserPermission(db.Model):
    __tablename__ = 'auth_user_user_permissions'
    __table_args__ = (
        db.Index('auth_user_user_permissions_user_id_permission_id_14a6b632_uniq', 'user_id', 'permission_id'),
    )

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.ForeignKey('auth_user.id'), nullable=False)
    permission_id = db.Column(db.ForeignKey('auth_permission.id'), nullable=False, index=True)

    permission = db.relationship('AuthPermission', primaryjoin='AuthUserUserPermission.permission_id == AuthPermission.id', backref='auth_user_user_permissions')
    user = db.relationship('AuthUser', primaryjoin='AuthUserUserPermission.user_id == AuthUser.id', backref='auth_user_user_permissions')


t_comp_view = db.Table(
    'comp_view',
    db.Column('comment', db.Text),
    db.Column('date', db.Date),
    db.Column('id', db.Integer, server_default=db.FetchedValue()),
    db.Column('num', db.Integer),
    db.Column('house', db.String(200)),
    db.Column('fio', db.String(200)),
    db.Column('name', db.String(200))
)


class DjangoAdminLog(db.Model):
    __tablename__ = 'django_admin_log'

    id = db.Column(db.Integer, primary_key=True)
    action_time = db.Column(db.DateTime, nullable=False)
    object_id = db.Column(db.String)
    object_repr = db.Column(db.String(200), nullable=False)
    action_flag = db.Column(db.SmallInteger, nullable=False)
    change_message = db.Column(db.String, nullable=False)
    content_type_id = db.Column(db.ForeignKey('django_content_type.id'), index=True)
    user_id = db.Column(db.ForeignKey('auth_user.id'), nullable=False, index=True)

    content_type = db.relationship('DjangoContentType', primaryjoin='DjangoAdminLog.content_type_id == DjangoContentType.id', backref='django_admin_logs')
    user = db.relationship('AuthUser', primaryjoin='DjangoAdminLog.user_id == AuthUser.id', backref='django_admin_logs')


class DjangoContentType(db.Model):
    __tablename__ = 'django_content_type'
    __table_args__ = (
        db.Index('django_content_type_app_label_model_76bd3d3b_uniq', 'app_label', 'model'),
    )

    id = db.Column(db.Integer, primary_key=True)
    app_label = db.Column(db.String(100), nullable=False)
    model = db.Column(db.String(100), nullable=False)


class DjangoMigration(db.Model):
    __tablename__ = 'django_migrations'

    id = db.Column(db.Integer, primary_key=True)
    app = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    applied = db.Column(db.DateTime, nullable=False)


class DjangoSession(db.Model):
    __tablename__ = 'django_session'

    session_key = db.Column(db.String(40), primary_key=True)
    session_data = db.Column(db.String, nullable=False)
    expire_date = db.Column(db.DateTime, nullable=False, index=True)


t_flat_view = db.Table(
    'flat_view',
    db.Column('flat', db.String(213)),
    db.Column('id', db.Integer, server_default=db.FetchedValue()),
    db.Column('h_id', db.Integer, server_default=db.FetchedValue())
)


t_req_view = db.Table(
    'req_view',
    db.Column('date', db.Date),
    db.Column('id', db.Integer, server_default=db.FetchedValue()),
    db.Column('comment', db.Text),
    db.Column('num', db.Integer),
    db.Column('fio', db.String(200)),
    db.Column('spec', db.String(403)),
    db.Column('house', db.String(200))
)


t_spec_view = db.Table(
    'spec_view',
    db.Column('name', db.String(402)),
    db.Column('id', db.Integer, server_default=db.FetchedValue())
)
