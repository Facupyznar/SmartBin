from app.database import db

class Lectura(db.Model):
    __tablename__ = 'Lectura'

    IDLectura = db.Column(db.Integer, primary_key=True)
    IDBin = db.Column(db.Integer, db.ForeignKey('Bin.IDBin'), nullable=False)
    peso = db.Column(db.Numeric(10, 2), nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())

    bin = db.relationship('Bin', backref='lecturas')

    def __repr__(self):
        return f'<Lectura Bin:{self.IDBin} - {self.peso}g @ {self.timestamp}>'
