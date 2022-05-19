# Imports
from flask import Flask, render_template

#------------------------------ Flask Setup ------------------------
app = Flask(__name__)

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

if __name__== '__main__':
    app.run(debug=True)
