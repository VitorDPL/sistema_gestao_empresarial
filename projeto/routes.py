from projeto import app, db
from flask import request, jsonify, render_template, redirect, url_for, flash
from projeto.models import *

@app.route('/')
def home():
    return render_template('index.html')


# login/ criação de usuário
@app.route('/fazer_login')
def fazer_login():
    return render_template('fazer_login.html')
    
@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    senha = request.form['senha']
    user = Usuario.query.filter_by(email=email).first()
    if user and user.senha == senha:
        flash(f'Bem-Vindo ao nosso sistema de gerenciamento, {user.nome}', 'success')
        return redirect(url_for('home'))
    flash('Credenciais inválidas', 'danger')
    return redirect(url_for('fazer_login'))

@app.route('/cadastrar_usuario', methods=['POST'])
def cadastrar_usuario():
    nome = request.form['nome']
    email = request.form['email']
    senha = request.form['senha']
    papel = request.form['papel']
    user = Usuario.query.filter_by(email=email).first()
    if user:
        flash('Usuário já existe', 'danger')
        return redirect(url_for('home'))
    new_user = Usuario(nome=nome, email=email, senha=senha, papel=papel)
    db.session.add(new_user)
    db.session.commit()
    flash(f'Usuário criado com sucesso, {new_user.nome}', 'success')
    return redirect(url_for('home'))

# alterações
@app.route('/alterar_usuario', methods=['GET'])
def alterar_usuario():
    usuarios = Usuario.query.all()
    return render_template('usuarios/alterar_usuario.html', usuarios=usuarios)

@app.route('/alterar_usuario/<int:id>', methods=['GET'])
def alterar_usuario_id(id):
    usuario = Usuario.query.get(id)
    return render_template('usuarios/alterar_usuario_id.html', usuario=usuario)

@app.route('/atualizar_usuario/<int:id>', methods=['POST'])
def atualizar_usuario(id):
    usuario = Usuario.query.get(id)
    usuario.nome = request.form['nome']
    usuario.email = request.form['email']
    usuario.papel = request.form['papel']
    db.session.commit()
    flash(f'Usuário {usuario.nome} atualizado com sucesso!', 'success')
    return redirect(url_for('alterar_usuario'))