from projeto import app, db
from flask import request, jsonify, render_template, redirect, url_for, flash, abort
from projeto.models import *
from flask_login import login_user, logout_user, login_required, current_user
from functools import wraps

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.papel != 'admin':
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
@login_required
@admin_required
def home():
    return render_template('index.html')

# Usuário
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
    return redirect(url_for('fazer_login'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Você saiu da sua conta.', 'success')
    return redirect(url_for('home'))

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

@app.route('/buscar_usuario', methods=['GET', 'POST'])
def buscar_usuario():
    nome = request.form.get('nome')
    user = Usuario.query.filter_by(nome=nome).first()
    return render_template('clientes/alterar_cliente.html', user=user)

# Cliente
@app.route('/cadastrar_cliente', methods=['GET', 'POST'])
@login_required
def cadastrar_cliente():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        telefone = request.form['telefone']
        endereco = request.form['endereco']
        numero = request.form['numero']
        bairro = request.form['bairro']
        complemento = request.form['complemento']
        cidade = request.form['cidade']
        estado = request.form['estado']
        cep = request.form['cep']
        
        novo_cliente = Cliente(nome=nome, email=email, telefone=telefone)
        db.session.add(novo_cliente)
        db.session.commit()
        
        novo_endereco = Endereco(cliente_id=novo_cliente.id, endereco=endereco, complemento=complemento, numero=numero, bairro=bairro, cidade=cidade, estado=estado, cep=cep)
        db.session.add(novo_endereco)
        db.session.commit()
        
        flash('Cliente cadastrado com sucesso!', 'success')
        return redirect(url_for('cadastrar_cliente'))
    return render_template('cadastros/cadastrar_clientes.html')

@app.route('/buscar_cliente', methods=['POST'])
@login_required
def buscar_cliente():
    nome = request.form.get('nome')
    cliente = Cliente.query.filter(Cliente.nome.like(f'%{nome}%')).first()
    if cliente:
        return jsonify({
            'cliente': {
                'id': cliente.id,
                'nome': cliente.nome,
                'email': cliente.email,
                'telefone': cliente.telefone
            }
        })
    return jsonify({'cliente': None})

@app.route('/alterar_cliente', methods=['GET', 'POST'])
@login_required
@admin_required
def alterar_cliente():
    nome = request.form.get('nome')
    telefone = request.form.get('telefone')
    query = Cliente.query

    if nome:
        query = query.filter(Cliente.nome.like(f'%{nome}%'))
    elif telefone:
        query = query.filter(Cliente.telefone.like(f'%{telefone}%'))

    clientes = query.all()

    return render_template('clientes/alterar_cliente.html', clientes=clientes)

# passa o id e renderiza o html alterar_cliente_id.html
@app.route('/alterar_cliente/<int:id>', methods=['GET'])
@login_required
@admin_required
def alterar_cliente_id(id):
    cliente = Cliente.query.get(id)
    return render_template('clientes/alterar_cliente_id.html', cliente=cliente)

# essa rota não renderiza nada, ela apenas faz as alterações e redireciona o usuário para outra página.
@app.route('/atualizar_cliente/<int:id>', methods=['POST'])
@login_required
def atualizar_cliente(id):
    cliente = Cliente.query.get_or_404(id)
    cliente.nome = request.form['nome']
    cliente.email = request.form['email']
    cliente.telefone = request.form['telefone']
    endereco = Endereco.query.filter_by(cliente_id=cliente.id).first()
    if endereco:
        endereco.endereco = request.form['endereco']
        endereco.cidade = request.form['cidade']
        endereco.estado = request.form['estado']
        endereco.cep = request.form['cep']
        endereco.complemento = request.form['complemento']
    else:
        novo_endereco = Endereco(
            cliente_id=cliente.id,
            endereco=request.form['endereco'],
            cidade=request.form['cidade'],
            estado=request.form['estado'],
            cep=request.form['cep'],
            complemento=request.form['complemento']
        )
        db.session.add(novo_endereco)
    db.session.commit()
    flash('Cliente atualizado com sucesso!', 'success')
    return redirect(url_for('alterar_cliente'))

# Produto
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
    categorias = Categoria.query.all()
    return render_template('cadastros/cadastrar_produtos.html', categorias=categorias)

@app.route('/cadastrar_categoria', methods=['POST'])
@login_required
def cadastrar_categoria():
    nome = request.form['nome']
    new_categoria = Categoria(nome=nome)
    db.session.add(new_categoria)
    db.session.commit()
    flash(f'Categoria {new_categoria.nome} cadastrada com sucesso!', 'success')
    return redirect(url_for('cadastrar_produto'))

@app.route('/buscar_produto', methods=['POST'])
@login_required
def buscar_produto():
    nome = request.form.get('nome')
    produtos = Produto.query.filter(Produto.nome.like(f'%{nome}%')).all()
    produtos_json = [{'id': produto.id, 'nome': produto.nome, 'preco': produto.preco} for produto in produtos]
    return jsonify({'produtos': produtos_json})

# Pedido
@app.route('/salvar_pedido', methods=['POST'])
@login_required
def salvar_pedido():
    data = request.json
    cliente_nome = data['cliente_nome']
    itens = data['itens']
    total = data['total']

    cliente = Cliente.query.filter_by(nome=cliente_nome).first()
    if not cliente:
        return jsonify({'success': False, 'message': 'Cliente não encontrado'})

    # Cria um novo pedido
    pedido = Pedido(usuario_id=cliente.id, total=total)
    db.session.add(pedido)
    db.session.commit()

    # Adiciona os itens ao pedido
    for item in itens:
        produto_id = item['produto_id']
        quantidade = item['quantidade']
        produto = Produto.query.get(produto_id)
        total_item = produto.preco * quantidade
        item_pedido = ItensPedido(produto_id=produto_id, pedido_id=pedido.id, quantidade=quantidade, total=total_item)
        db.session.add(item_pedido)

    db.session.commit()

    return jsonify({'success': True})

@app.errorhandler(403)
def forbidden(e):
    return render_template('403.html'), 403