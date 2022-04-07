from config import db
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

class User(db.Model): 
    __tablename__ = 'users'
    
    # Columns
    
    id = db.Column(
        db.Integer,
        primary_key = True
    )
    
    username = db.Column(
        db.String(255),
        unique=True,
        nullable=False
    )

    password = db.Column(
        db.String(255),
        nullable=False
    )

    firstname = db.Column(
        db.String(255),
        nullable=False
    )
    
    lastname = db.Column(
        db.String(255),
        nullable=False
    )

    email = db.Column(
        db.String(255),
        unique=True,
        nullable=False
    )
    
    user_type_id = db.Column(
        db.Integer,
        db.ForeignKey('user_types.id'),
        nullable=False
    )
    
    created_at = db.Column(
        db.DateTime,
        default = datetime.utcnow,
        nullable=False
    )
    
    def __init__(self, username, email, firstname, lastname, password, created_at, user_type_id):
        self.username = username
        self.email = email
        self.created_at = created_at or datetime.utcnow()
        self.firstname = firstname
        self.lastname = lastname
        self.user_type_id = user_type_id
        self.password = generate_password_hash(
            password, method='pbkdf2:sha256')

    def check_password(self, password):
        return check_password_hash(self.password, password)


class UserType(db.Model):
    __tablename__ = 'user_types'
    
    # Columns
    
    id = db.Column(
        db.Integer,
        primary_key = True
    )
    
    user_type_name = db.Column(
        db.String(255),
        unique=True,
        nullable=False
    )
    
    users = db.relationship('User')
    
    def __init__(self,user_type_name) -> None:
        self.user_type_name = user_type_name

