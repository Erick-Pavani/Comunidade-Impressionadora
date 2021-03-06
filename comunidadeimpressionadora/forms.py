# Imports
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from comunidadeimpressionadora.models import Usuario
from flask_login import current_user

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

# Editar Perdil
class FormEditarPerfil(FlaskForm):
    username = StringField('Novo nome do usuário', validators = [DataRequired(message = "Digite um nome de usuário!")])
    email = StringField('Novo e-mail', validators = [DataRequired(message = "Digite um email!"), Email(message = "Digite um email válido!")])
    foto_perfil = FileField('Atualizar foto de perfil', validators = [FileAllowed(['jpg', 'png', 'jpeg'], message = "Somente arquivos no formato '.jpg' e '.png' são aceitos!")])
    curso_excel = BooleanField('Excel Impressionador')
    curso_powerbi = BooleanField('PowerBI Impressionador')
    curso_vba = BooleanField('VBA Impressionador')
    curso_python = BooleanField('Python Impressionador')
    curso_sql = BooleanField('SQL Impressionador')
    curso_ppt = BooleanField('Apresentações Impressionadoras')
    botao_editar_perfil = SubmitField('Confirmar Edição')

    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email = email.data).first()
        if not current_user.email == email.data and usuario:
            raise ValidationError("Esse email já está cadastrado em nosso site!")

class FormCriarPost(FlaskForm):
    titulo = StringField('Titulo do Post', validators=[DataRequired(message = "Dê um título ao seu post!"), Length(2, 140, message = "O título deve possuir de 2 a 140 caracteres!")])
    corpo = TextAreaField('Escreva seu post aqui', validators=[DataRequired(message = "Preencha o seu post!")])
    botao_criar_post = SubmitField('Publicar Post')