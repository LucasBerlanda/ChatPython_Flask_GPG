from app import db, app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login

class Usuario(UserMixin, db.Model):
    
    __tablename__ = "usuario"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    username = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    status = db.Column(db.Boolean)
    
    def __init__(self, name, email ,username, password_hash, status):
        
        self.name = name
        self.email = email
        self.username = username
        self.password_hash = password_hash
        self.status = status
            
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)    

class Mensagem(db.Model):
    
    __tablename__ = "mensagem"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    body = db.Column(db.String(1000))
    msg_by = db.Column(db.Integer)
    msg_to = db.Column(db.Integer)

    def __init__(self, body, msg_by, msg_to):
        
        self.body = body
        self.msg_by = msg_by
        self.msg_to = msg_to
    
@login.user_loader
def load_user(id):
    return Usuario.query.get(int(id))  
        
    
db.create_all()