# Imports
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from comunidadeimpressionadora.models import Usuario

#-------------------- Classes----------------------

# Login
class FormLogin(FlaskForm):
    email = StringField('E-mail', validators = [DataRequired(message = "Digite um nome de usuário!"), Email(message = "Digite um email válido!")])
    senha = PasswordField('Senha', validators = [DataRequired(message = "Digite uma senha!"), Length(6, 20, message = "A senha deve conter de 6 a 20 caracteres!")])
    lembrar_dados = BooleanField('Lembrar senha')
    botao_login = SubmitField('Fazer Login')

# Criar Conta
class FormCriarConta(FlaskForm):
    username = StringField('Nome do usuário', validators = [DataRequired(message = "Digite um nome de usuário!")])
    email = StringField('E-mail', validators = [DataRequired(message = "Digite um email!"), Email(message = "Digite um email válido!")])
    senha = PasswordField('Senha', validators = [DataRequired(message = "Digite uma senha!"), Length(6, 20, message = "Digite uma senha de 6 a 20 caracteres!")])
    confirmacao = PasswordField('Confirme a senha', validators = [DataRequired(message = "Digite a mesma senha usada no campo acima!"), EqualTo('senha', message = "As senhas devem ser iguais!")])
    botao_criar_conta = SubmitField('Criar conta')

    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email = email.data).first()
        if usuario:
            raise ValidationError("Esse email já está cadastrado em nosso site!")
