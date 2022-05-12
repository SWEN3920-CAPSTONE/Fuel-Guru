from werkzeug.security import check_password_hash, generate_password_hash
from config import db
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method

class InvalidToken(db.Model):
    
    __tablename__ = 'invalid_tokens'
    
    jti = db.Column(
        db.String(500),
        primary_key=True,
        nullable=False
    )
    
    expiry_date = db.Column(
        db.DateTime,
        nullable=False
    )
    
    def __init__(self, jti, expiry_date) -> None:
        self.jti = jti
        self.expiry_date = expiry_date
