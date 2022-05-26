from flask import render_template, url_for, redirect, request, flash, abort
from comunidadeimpressionadora import app, database, bcrypt
from comunidadeimpressionadora.forms import FormLogin, FormCriarConta, FormEditarPerfil, FormCriarPost
from comunidadeimpressionadora.models import Post, Usuario
from flask_login import login_user, logout_user, current_user, login_required
import os
import secrets
from PIL import Image

#------------------------------ Flask Routes -----------------------

# Home
@app.route('/')
def home():
    posts = Post.query.order_by(Post.id.desc())
    return render_template('home.html', posts = posts)

# Contato
@app.route('/contato')
def contato():
    return render_template('contato.html')

# Contato
@app.route('/usuarios')
@login_required
def usuarios():
    return render_template('usuarios.html', lista_usuarios = Usuario.query.all())

# Login
@app.route('/login', methods = ['GET', 'POST'])
def login():
    form_login = FormLogin()
    form_criar_conta = FormCriarConta()
    
    if form_login.validate_on_submit() and 'botao_login' in request.form:
        usuario = Usuario.query.filter_by(email = form_login.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha.encode('utf-8'), form_login.senha.data):
            login_user(usuario, remember = form_login.lembrar_dados.data)
            flash(f'Login realizado com sucesso no email {form_login.email.data}', 'alert-success')
            par_next = request.args.get('next')
            if par_next:
                return redirect(par_next)
            else:
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
@app.route('/post/criar', methods = ['GET', 'POST'])
@login_required
def criar_post():
    form = FormCriarPost()
    if form.validate_on_submit():
        post = Post(titulo = form.titulo.data, corpo = form.corpo.data, autor = current_user)
        database.session.add(post)
        database.session.commit()
        flash('Post publicado com sucesso!', 'alert-success')
        return redirect(url_for('home'))
    return render_template('criarpost.html', form = form)

# Perfil
@app.route('/perfil')
@login_required
def perfil():
    foto_perfil = url_for('static', filename = f'fotos_perfil/{current_user.foto_perfil}')
    
    return render_template('perfil.html', foto_perfil = foto_perfil)

# Editar Perfil
@app.route('/perfil/editar', methods = ['GET', 'POST'])
@login_required
def editar_perfil():
    form = FormEditarPerfil() 
    if request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        for curso in current_user.cursos.split(';'):
            for campo in form:
                if curso in campo.label.text:
                    campo.data = True
                    break
    elif form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        if form.foto_perfil.data:
            current_user.foto_perfil = salvar_imagem(form.foto_perfil.data)
        current_user.cursos = atualizar_cursos(form)
        database.session.commit()
        flash('Seu perfil foi atualizado com sucesso!', 'alert-success')
        return redirect(url_for('perfil'))
    foto_perfil = url_for('static', filename = f'fotos_perfil/{current_user.foto_perfil}')
    return render_template('editar_perfil.html', foto_perfil = foto_perfil, form = form)

# Exibir Post
@app.route('/post/<post_id>', methods = ['GET', 'POST'])
@login_required
def exibir_post(post_id):
    post = Post.query.get(post_id)
    if current_user == post.autor:
        form = FormCriarPost()
        if request.method == 'GET':
            form.titulo.data = post.titulo
            form.corpo.data = post.corpo
        elif form.validate_on_submit():
            post.titulo = form.titulo.data
            post.corpo = form.corpo.data
            database.session.commit()
            flash('Post atualizado com sucesso!', 'alert-success')

            return redirect(url_for('home'))
    else:
        form = None

    return render_template('post.html', post = post, form = form)

# Excluir Post
@app.route('/post/<post_id>/excluir', methods = ['GET', 'POST'])
@login_required
def excluir_post(post_id):
    post = Post.query.get(post_id)
    if current_user == post.autor:
        database.session.delete(post)
        database.session.commit()
        flash('Post excluído!', 'alert-danger')
        
        return redirect(url_for('home'))
    else:
        abort(403)

@app.route('/perfil/excluir')
@login_required
def excluir_user():
    user_id = current_user.id
    user_foto = current_user.foto_perfil
    caminho = os.path.join(app.root_path, 'static/fotos_perfil')
    fotos = os.listdir(caminho)
    for foto in fotos:
        if user_foto in foto:
            os.remove(os.path.join(app.root_path, 'static/fotos_perfil', foto))
    user = Usuario.query.get(user_id)
    posts = Post.query.filter_by(id_usuario = user_id).all()
    database.session.delete(user)
    for post in posts:
        database.session.delete(post)
    database.session.commit()
    flash('Seu usuário foi excluído permanentemente! Aguardamos o seu retorno um dia!', 'alert-danger')

    return redirect(url_for('home'))
#-----------------------------------  Funções -----------------------------------------

# Salvar a foto de perfil
def salvar_imagem(imagem):
    nome, extensao = os.path.splitext(imagem.filename)
    email = current_user.email.split('.')[0]
    caminho = os.path.join(app.root_path, 'static/fotos_perfil')
    fotos = os.listdir(caminho)
    for foto in fotos:
        if email in foto:
            os.remove(os.path.join(app.root_path, 'static/fotos_perfil', foto))
    nome_arquivo = email + extensao
    caminho_completo = os.path.join(app.root_path, 'static/fotos_perfil', nome_arquivo)
    tamanho = (200, 200)
    imagem_reduzida = Image.open(imagem)
    imagem_reduzida.thumbnail(tamanho)
    imagem_reduzida.save(caminho_completo)
    
    return nome_arquivo

# Atualizar Cursos
def atualizar_cursos(form):
    lista_cursos = ['Não informado']
    counter = 0
    for campo in form:
        if 'curso_' in campo.name and campo.data:
            if counter == 0:
                lista_cursos = []
            counter += 1
            if 'Apresentações' in campo.label.text:
                lista_cursos.append(campo.label.text.split(' ')[0])
            else:
                lista_cursos.append(campo.label.text)
    
    return ';'.join(lista_cursos)