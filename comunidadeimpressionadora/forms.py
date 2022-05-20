# Imports
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo

#-------------------- Classes----------------------

# Login
class FormLogin(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(6, 20)])
    lembrar_dados = BooleanField('Lembrar senha')
    botao_login = SubmitField('Fazer Login')

# Criar Conta
class FormCriarConta(FlaskForm):
    username = StringField('Nome do usuário', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(6, 20)])
    confirmacao = PasswordField('Confirme a senha', validators=[DataRequired(), EqualTo('senha')])
    botao_criar_conta = SubmitField('Criar conta')
