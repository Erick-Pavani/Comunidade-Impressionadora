from flask import render_template, url_for, redirect, request, flash
from comunidadeimpressionadora import app
from comunidadeimpressionadora.forms import FormLogin, FormCriarConta

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
def usuarios():
    return render_template('usuarios.html', lista_usuarios = lista_usuarios)

# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    form_login = FormLogin()
    form_criar_conta = FormCriarConta()
    
    if form_login.validate_on_submit() and 'botao_login' in request.form:
        flash(f'Login realizado com sucesso no email {form_login.email.data}', 'alert-success')
        
        return redirect(url_for('home'))
    
    if form_criar_conta.validate_on_submit() and 'botao_criar_conta' in request.form:
        flash(f'Conta criada com sucesso usando o email {form_criar_conta.email.data}', 'alert-success')
        
        return redirect(url_for('home'))
    
    return render_template('login.html', form_login = form_login, form_criar_conta = form_criar_conta)
