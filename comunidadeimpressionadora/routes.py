from flask import render_template, url_for, redirect, request, flash
from comunidadeimpressionadora import app, database, bcrypt
from comunidadeimpressionadora.forms import FormLogin, FormCriarConta
from comunidadeimpressionadora.models import Usuario
from flask_login import login_user, logout_user, current_user, login_required

#------------------------------ Flask Routes -----------------------

lista_usuarios = ['Erick', 'Gabi', 'Pingo']

# Home
@app.route('/')
def home():
    return render_template('home.html')

# Contato
@app.route('/contato')
def contato():
    return render_template('contato.html')

# Contato
@app.route('/usuarios')
@login_required
def usuarios():
    return render_template('usuarios.html', lista_usuarios = lista_usuarios)

# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    form_login = FormLogin()
    form_criar_conta = FormCriarConta()
    
    if form_login.validate_on_submit() and 'botao_login' in request.form:
        usuario = Usuario.query.filter_by(email = form_login.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha.encode('utf-8'), form_login.senha.data):
            login_user(usuario, remember = form_login.lembrar_dados.data)
            flash(f'Login realizado com sucesso no email {form_login.email.data}', 'alert-success')
            return redirect(url_for('home'))
        else:
            flash(f'Seu usuário ou senha estão incorretos! Tente novamente!', 'alert-danger')
    
    elif form_criar_conta.validate_on_submit() and 'botao_criar_conta' in request.form:
        flash(f'Conta criada com sucesso usando o email {form_criar_conta.email.data}', 'alert-success')
        senha_crypt = bcrypt.generate_password_hash(form_criar_conta.senha.data).decode('utf-8')
        usuario = Usuario(username = form_criar_conta.username.data, email = form_criar_conta.email.data, senha = senha_crypt)
        database.session.add(usuario)
        database.session.commit()
        
        return redirect(url_for('home'))
    
    return render_template('login.html', form_login = form_login, form_criar_conta = form_criar_conta)

# Sair
@app.route('/sair')
@login_required
def sair():
    logout_user()
    flash(f'Logout realizado com sucesso!', "alert-success")
    
    return redirect(url_for('home'))

# Criar Post
@app.route('/post/criar')
@login_required
def criarpost():
    return render_template('criarpost.html')

# Perfil
@app.route('/perfil')
@login_required
def perfil():
    return render_template('perfil.html')