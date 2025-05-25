from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app.database import db

class User(db.Model, UserMixin):
    __tablename__ = 'User'

    IDUser = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __init__(self, nombre, email, password):
        self.nombre = nombre
        self.email = email
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def id(self):
        return self.IDUser

    def get_id(self):
        return str(self.IDUser)

    # ----- Métodos de clase unificados -----

    @classmethod
    def login(cls, nombre, password):
        user = cls.query.filter_by(nombre=nombre).first()
        if user and user.check_password(password):
            return user
        return None

    @classmethod
    def register(cls, nombre, email, password):
        if cls.query.filter_by(nombre=nombre).first():
            raise Exception("El nombre de usuario ya está en uso.")
        if cls.query.filter_by(email=email).first():
            raise Exception("El email ya está registrado.")
        if len(password) < 6:
            raise Exception("La contraseña debe tener al menos 6 caracteres.")
        new_user = cls(nombre=nombre, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        return new_user
