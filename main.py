# Imports
from flask import Flask, render_template

# Flask Setup
app = Flask(__name__)

# Flask Routes
@app.route('/')
def home():
    return render_template('home.html')


@app.route('/contato')
def contato():
    return render_template('contato.html')

if __name__== '__main__':
    app.run(debug=True)
