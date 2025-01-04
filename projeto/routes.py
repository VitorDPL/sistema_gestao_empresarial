from projeto import app, db
from flask import request, jsonify, render_template, redirect, url_for, flash, abort
from projeto.models import *
from flask_login import login_user, logout_user, login_required, current_user
from functools import wraps

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.papel != 'admin':
            abort(403)  # Forbidden
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
@login_required
@admin_required
def home():
    return render_template('index.html')

# usuário
@app.route('/fazer_login')
def fazer_login():
    return render_template('usuarios/fazer_login.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    senha = request.form['senha']
    user = Usuario.query.filter_by(email=email).first()
    if user and user.senha == senha:
        login_user(user)
        flash(f'Bem-Vindo ao nosso sistema de gerenciamento, {user.nome}', 'success')
        return redirect(url_for('home'))
    flash('Credenciais inválidas', 'danger')
    return redirect(url_for('usuarios/fazer_login'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Você saiu da sua conta.', 'success')
    return redirect(url_for('home'))

@app.route('/cadastrar_usuario', methods=['POST'])
@login_required
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

@app.route('/buscar_usuario', methods=['GET', 'POST'])
def buscar_usuario():
    nome = request.form.get('nome')
    user = Usuario.query.filter_by(nome = nome ).first()
    return render_template('usuarios/alterar_cliente.html', user=user)

# alterações
@app.route('/alterar_cliente', methods=['GET', 'POST'])
@login_required
@admin_required
def alterar_cliente():
    usuarios = Cliente.query.all()

    nome = request.form.get('nome')
    telefone = request.form.get('telefone')
    
    if nome:
        usuarios = Cliente.query.filter(Cliente.nome.like(f'%{nome}%')).all()
    elif telefone:
        usuarios = Cliente.query.filter(Cliente.telefone.like(f'%{telefone}%')).all()

    return render_template('usuarios/alterar_cliente.html', usuarios=usuarios)

@app.route('/alterar_cliente/<int:id>', methods=['GET'])
@login_required
@admin_required
def alterar_cliente_id(id):
    usuario = Cliente.query.get(id)
    return render_template('usuarios/alterar_cliente_id.html', usuario=usuario)

@app.route('/atualizar_usuario/<int:id>', methods=['POST'])
@login_required
@admin_required
def atualizar_usuario(id):
    usuario = Cliente.query.get(id)
    
    usuario.nome = request.form['nome']
    usuario.email = request.form['email']
    usuario.telefone = request.form['telefone']
    usuario.endereco = request.form['endereco']
    usuario.cidade = request.form['cidade']
    usuario.estado = request.form['estado']
    usuario.cep = request.form['cep']

    db.session.commit()
    flash(f'Usuário {usuario.nome} atualizado com sucesso!', 'success')
    return redirect(url_for('alterar_cliente'))

@app.errorhandler(403)
def forbidden(e):
    return render_template('403.html'), 403

# criaçao de clientes
@app.route('/cadastrar_cliente')
@login_required
def template_cadastrar_cliente():
    return render_template('cadastros/cadastrar_clientes.html')

@app.route('/fazer_cadastro_de_clientes', methods=['POST'])
@login_required
def cadastrar_cliente():
    nome = request.form['nome']
    email = request.form['email']
    telefone = request.form['telefone']
    endereco = request.form['endereco']
    cidade = request.form['cidade']
    estado = request.form['estado']
    cep = request.form['cep']
    new_cliente = Cliente(nome=nome, email=email, telefone=telefone, endereco=endereco, cidade=cidade, estado=estado, cep=cep)
    db.session.add(new_cliente)
    db.session.commit()
    flash(f'Cliente {new_cliente.nome} cadastrado com sucesso!', 'success')
    return redirect(url_for('home'))

# cadastro de produtos
@app.route('/cadastrar_produto')
@login_required
def template_cadastrar_produto():
    categorias = Categoria.query.all()
    return render_template('cadastros/cadastrar_produtos.html', categorias=categorias)

@app.route('/cadastrar_produto', methods=['GET', 'POST'])
@login_required
def cadastrar_produto():
    if request.method == 'POST':
        nome = request.form['nome']
        preco = request.form['preco']
        quantidade = request.form['quantidade']
        categoria_id = request.form['categoria_id']
        new_produto = Produto(nome=nome, preco=preco, quantidade=quantidade, categoria_id=categoria_id)
        db.session.add(new_produto)
        db.session.commit()
        flash(f'Produto {new_produto.nome} cadastrado com sucesso!', 'success')
        return redirect(url_for('cadastrar_produto'))
    return render_template('cadastrar_produto.html')

@app.route('/cadastrar_categoria', methods=['POST'])
@login_required
def cadastrar_categoria():
    nome = request.form['nome']
    new_categoria = Categoria(nome=nome)
    db.session.add(new_categoria)
    db.session.commit()
    flash(f'Categoria {new_categoria.nome} cadastrada com sucesso!', 'success')
    print("-------------------")
    return redirect(url_for('cadastrar_produto'))

@app.route('/buscar_produto', methods=['POST'])
@login_required
def buscar_produto():
    nome = request.form.get('nome')
    produtos = Produto.query.filter(Produto.nome.like(f'%{nome}%')).all()
    return render_template('index.html', produtos=produtos)