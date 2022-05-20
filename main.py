# Imports
from flask import Flask, render_template, url_for
from forms import FormLogin, FormCriarConta

#------------------------------ Flask Setup ------------------------
app = Flask(__name__)

app.config['SECRET_KEY'] = '4c673c0ef7953896bc739e5c6161b2ad'

#-------------------------------------------------------------------

lista_usuarios = ['Erick', 'Gabi', 'Gabriele', 'Sandra', 'Pingo']

#------------------------------ Flask Routes -----------------------

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
    return render_template('login.html', form_login = form_login, form_criar_conta = form_criar_conta)

if __name__== '__main__':
    app.run(debug=True)
