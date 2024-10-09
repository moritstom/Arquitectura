from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    puntos_interes = db.relationship('PuntoDeInteres')
    eventos = db.relationship('Evento')

class PuntoDeInteres(db.Model):
    id = db.Column(db.Integer, primary_key=True,nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text, nullable=True)
    latitud = db.Column(db.Float, nullable=False)
    longitud = db.Column(db.Float, nullable=False)
    imagenes = db.Column(db.String(100), nullable=True)
    fecha_creacion = db.Column(db.DateTime(timezone=True), default=func.now())
    tipo = db.Column(db.String(100), nullable=False)
    apertura = db.Column(db.String(100), nullable=True)
    cierre = db.Column(db.String(100), nullable=True)
    
class Evento(db.Model):
    id = db.Column(db.Integer, primary_key=True,nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text, nullable=True)
    latitud = db.Column(db.Float, nullable=False)
    longitud = db.Column(db.Float, nullable=False)
    imagenes = db.Column(db.String(100), nullable=True)
    fecha_creacion = db.Column(db.DateTime(timezone=True), default=func.now())
    tipo = db.Column(db.String(100), nullable=False)
    fecha_inicio = db.Column(db.DateTime(timezone=True), nullable=False)
    hora_inicio = db.Column(db.String(100), nullable=False)
    hora_fin = db.Column(db.String(100), nullable=False)