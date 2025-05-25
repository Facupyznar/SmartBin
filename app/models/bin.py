from app.database import db

class Bin(db.Model):
    __tablename__ = 'Bin'

    IDBin = db.Column(db.Integer, primary_key=True)
    IDUser = db.Column(db.Integer, db.ForeignKey('User.IDUser'), nullable=False)
    uid_hardware = db.Column(db.String(50), unique=True, nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    ubicacion = db.Column(db.String(100), nullable=True)
    fecha_creacion = db.Column(db.DateTime, default=db.func.current_timestamp())

    # Relación opcional con User (si la querés usar desde el modelo)
    user = db.relationship('User', backref='bins')

    def __repr__(self):
        return f'<Bin {self.nombre} ({self.uid_hardware})>'
    
    @property
    def ultima_lectura(self):   
        return max(self.lecturas, key=lambda l: l.timestamp, default=None)