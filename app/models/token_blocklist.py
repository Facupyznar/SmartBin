from app.database import db

class TokenBlocklist(db.Model):
    __tablename__ = 'TokenBlocklist'

    IDToken = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(255), nullable=False, unique=True)
    fecha_revocado = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f'<TokenBlocklist {self.jti} - revocado el {self.fecha_revocado}>'
