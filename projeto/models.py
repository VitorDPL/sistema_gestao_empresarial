from projeto import db
from datetime import datetime
from flask_login import UserMixin

class Usuario(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    senha = db.Column(db.String(200), nullable=False)
    papel = db.Column(db.String(50), default='cliente')

class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, default="Sem email")
    telefone = db.Column(db.String(20), nullable=False)
    endereco = db.Column(db.String(200), nullable=False)
    cidade = db.Column(db.String(100), nullable=False)
    estado = db.Column(db.String(50), nullable=False)
    cep = db.Column(db.String(20), nullable=False)

class Categoria(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    produtos = db.relationship('Produto', backref='categoria', lazy=True)

class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    preco = db.Column(db.Float, nullable=False)
    quantidade = db.Column(db.Integer, default=0)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categoria.id'), default="Sem categoria")

class Venda(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    produto_id = db.Column(db.Integer, db.ForeignKey('produto.id'))
    pedido_id = db.Column(db.Integer, db.ForeignKey('pedido.id'))
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    desconto = db.Column(db.Float, nullable=False)
    data_venda = db.Column(db.DateTime, default=datetime)
    quantidade = db.Column(db.Integer, nullable=False)
    valor_frete = db.Column(db.Float, nullable=False)

    total = db.Column(db.Float, nullable=False)

class Pedido(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    data_criacao = db.Column(db.DateTime, default=datetime)
    total = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), default='Pendente')

class Lancamento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(200), nullable=False)
    valor = db.Column(db.Float, nullable=False)
    tipo = db.Column(db.String(50))  # Entrada ou Saída
    data = db.Column(db.DateTime, default=datetime)
