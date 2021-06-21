from sqlalchemy.sql.expression import null
from sqlalchemy.sql.sqltypes import Boolean
from flask_login import UserMixin
from sqlalchemy import Column, Integer, String
from passlib.hash import pbkdf2_sha256
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from config import TestConfig as config
from .. import db, login_manager

# User Model
class User(db.Model, UserMixin):

    __tablename__ = 'User'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    password = Column(String)
    is_member = Column(Boolean, default=False)
    membership_type = Column(String, nullable=True)

    def check_password(self, password):
        return pbkdf2_sha256.verify(password, self.password)
    
    def set_password(self, password):
        self.password = pbkdf2_sha256.hash(password)

    def generate_reset_token(self):
        s = Serializer(config.SECRET_KEY, config.RESET_EXPIRATION_TIME)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @classmethod
    def verify_reset_token(cls, token):
        s = Serializer(config.SECRET_KEY)
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        
        return cls.query.get(user_id)

@login_manager.user_loader
def user_loader(id):
    return User.query.filter_by(id=id).first()

@login_manager.request_loader
def request_loader(request):
    email = request.form.get('email')
    user = User.query.filter_by(email=email).first()
    return user if user else None

