from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

# flask
app = Flask(__name__)
# sqlalchemy com sqlite
path = os.path.dirname(os.path.abspath(__file__))
arquivobd = os.path.join(path, 'casa_heranca.db')
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///"+arquivobd
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # remover warnings
db = SQLAlchemy(app)

class Casa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    formato = db.Column(db.String(254))
    quartos = db.relationship("Quarto", backref="casa")

    def __repr__(self):
        s = f"ID: {self.id}, Formato: {self.formato}"
        if len(self.quartos) > 0:
            s += f"\nQuartos:"
            for q in self.quartos:
                s += f"\n - {str(q)}"
        return s

class Quarto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(254))
    dimensoes= db.Column(db.String(254))
    casa_id = db.Column(db.Integer, db.ForeignKey(Casa.id), nullable=False)
    mobilias = db.relationship("Mobilia", backref="quarto")

    def __repr__(self):
        s = f"ID: {self.id}, Nome: {self.nome}, Dimensões: {self.dimensoes}"
        if len(self.mobilias) > 0:
            s += "\n  Mobílias:"
            for m in self.mobilias:
                s += f"\n    - {str(m)}"
        return s

class Mobilia(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(254))
    funcao = db.Column(db.String(254))
    material = db.Column(db.String(254))
    quarto_id = db.Column(db.Integer, db.ForeignKey(Quarto.id), nullable=True)
    tipo = db.Column(db.String(50))
    __mapper_args__ = {
        "polymorphic_identity": "mobilia",
        "polymorphic_on": tipo
    }

    def __repr__(self):
        return f"ID: {self.id}, nome: {self.nome}, funcao: {self.funcao}, material: {self.material}"

class Eletrodomestico(Mobilia):
    marca = db.Column(db.String(254))
    consumo = db.Column(db.String(254))
    id = db.Column(db.Integer, db.ForeignKey(Mobilia.id), primary_key=True)
    __mapper_args__ = {
        "polymorphic_identity": "eletrodomestico"
    }

    def __repr__(self):
        return super().__repr__() + f", consumo: {self.consumo}, marca: {self.marca}"

if __name__ == "__main__":
    db.create_all()
    
    c1 = Casa(formato="Russa")
    db.session.add(c1)
    db.session.commit()

    sala = Quarto(nome="sala", dimensoes="3x4m", casa=c1)
    db.session.add(sala)
    db.session.commit()

    cozinha = Quarto(nome="cozinha", dimensoes="5x6m", casa=c1)
    db.session.add(sala)
    db.session.commit()
    #print(q1.casa.formato)

    geladeira = Eletrodomestico(nome="geladeira tsunami 2 portas", funcao="refrigerar", material="aço", consumo="48 kWh mensal", marca="eletrolux", quarto=cozinha)
    db.session.add(geladeira)
    db.session.commit()

    print(c1)