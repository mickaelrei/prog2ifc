from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

# flask
app = Flask(__name__)
# sqlalchemy com sqlite
path = os.path.dirname(os.path.abspath(__file__))
arquivobd = os.path.join(path, 'pessoas.db')
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///"+arquivobd
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # remover warnings
db = SQLAlchemy(app)

class Pessoa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(254))
    email = db.Column(db.String(254))
    telefone = db.Column(db.String(254))
    tipo = db.Column(db.String(50))
    __mapper_args__ = {
        "polymorphic_identity": "pessoa",
        "polymorphic_on": tipo
    }

    def __repr__(self) -> str:
        return f"{self.id}, {self.nome}, {self.email}, {self.telefone}"

class Vendedor(Pessoa):
    comissao = db.Column(db.String(254))
    id = db.Column(db.Integer, db.ForeignKey(Pessoa.id), primary_key=True)
    __mapper_args__ = {
        "polymorphic_identity": "vendedor"
    }

    def __repr__(self) -> str:
        return super().__repr__() + f", {self.comissao}"

class Motorista(Pessoa):
    cnh = db.Column(db.String(254))
    id = db.Column(db.Integer, db.ForeignKey(Pessoa.id), primary_key=True)
    __mapper_args__ = {
        "polymorphic_identity": "motorista"
    }

    def __repr__(self) -> str:
        return super().__repr__() + f", {self.cnh}"

if __name__ == "__main__":
    db.create_all()

    pedro = Vendedor(nome="Pedro", email="pe@gmail.com", comissao="10")
    print(pedro)
    db.session.add(pedro)
    db.session.commit()
  
    teresa = Motorista(nome="Teresa", cnh="1234-5")
    print()
    print(teresa)
    db.session.add(teresa)
    db.session.commit()