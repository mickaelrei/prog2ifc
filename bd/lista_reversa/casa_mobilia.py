from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

# flask
app = Flask(__name__)
# sqlalchemy com sqlite
path = os.path.dirname(os.path.abspath(__file__))
arquivobd = os.path.join(path, 'imobiliaria.db')
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///"+arquivobd
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # remover warnings
db = SQLAlchemy(app)

class Casa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    formato = db.Column(db.String(254))
    quartos = db.relationship("Quarto", backref="casa")

    def __repr__(self):
        s = f"{self.id}, {self.formato}"
        for q in self.quartos:
            s += str(q)
        return s

class Quarto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(254))
    dimensoes= db.Column(db.String(254))
    casa_id = db.Column(db.Integer, db.ForeignKey(Casa.id), nullable=False)
    mobilias = db.relationship("Mobilia", backref="quarto")
    #casa = db.Relationship("Casa")

    def __repr__(self):
        s = f"{self.id}, {self.nome}, {self.dimensoes}"
        for m in self.mobilias:
            s += str(m)
        return s

class Mobilia(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(254))
    funcao = db.Column(db.String(254))
    material = db.Column(db.String(254))
    quarto_id = db.Column(db.Integer, db.ForeignKey(Quarto.id), nullable=True)

    def __repr__(self):
        return f"{self.id}, {self.nome}, {self.funcao}, {self.material}"

if __name__ == "__main__":
    db.create_all()
    
    c1 = Casa(formato="Russa")
    db.session.add(c1)
    db.session.commit()
    print(c1)

    q1 = Quarto(nome="sala", dimensoes="3x4m", casa=c1)
    db.session.add(q1)
    db.session.commit()
    print(q1.casa.formato)

    # Mostra todos os quartos da sessão
    for q in db.session.query(Quarto).all():
        print(q)

    # Mostra todos os quartos da casa 1
    '''for q in db.session.query(Quarto).filter(Quarto.casa_id=c1.id).all():
        print(q)'''

    for q in c1.quartos:
        print(q)