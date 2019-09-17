from flask import render_template, url_for, redirect, request, flash 
from app import app, db
from app.forms import LoginForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import Usuario, Mensagem
from werkzeug.urls import url_parse

@app.route("/index")
@login_required
def index():
    users = Usuario.query.all()
    
    return render_template("chat_room.html", users=users)

@app.route('/', methods=['GET', 'POST'])
def login():
    
    if current_user.is_authenticated: #verifico se o usuario está logado ou não
        return redirect(url_for('index')) 
    form = LoginForm()
    if form.validate_on_submit():
        user = Usuario.query.filter_by(username = form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Usuário ou senha incorretos!')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        db.session.query(Usuario).filter(Usuario.id == user.id).update({'status': True})
        db.session.commit()
        if not next_page or url_parse(next_page).netloc != '': #se tiver valor que não pertença a url principal
            next_page = url_for('index')
        return redirect(next_page) #se tiver ele direciona para onde foi solicitado
    return render_template('login.html', form=form, title="Login")

@app.route('/logout')
def logout():
    userlogado = current_user.id
    logout_user()
    db.session.query(Usuario).filter(Usuario.id == userlogado).update({'status': False})
    db.session.commit()
    return redirect(url_for('login'))


# @app.route('/chatting/<int:id>', methods=['GET', 'POST'])
# def chatting(id):
#     if current_user :
#         form = MessageForm()

#         usuario = Usuario.query.filter_by(id = id).first()
        
#         if usuario:
            
#             session_name = usuario.name
#             session_uid = current_user.id
#             session_lid = id

#             if request.method == 'POST' and form.validate():
#                 txt_body = form.body.data

#                 mensagem = Mensagem(body=txt_body, msg_by=msgMinha, msg_to= uid)
#                 db.session.add(mensagem)
#                 db.session.commit()
                
#             users = Usuario.query.all()
            
#             return render_template('chat_room.html', users=users, form=form)
#         else:
#             flash('No permission!', 'danger')
#             return redirect(url_for('index'))
#     else:
#         return redirect(url_for('login'))

# @app.route('/chats', methods=['GET', 'POST'])
# def chats():
#     if current_user:
#         # id = session_lid
#         # uid = current_user.id
#         id = session['lid']
#         uid = session['uid']
        
#         #chats = Mensagem.query.filter(msg_by=id and msg_to=uid).filter(msg_by=uid and msg_to=id)
#         chats = Mensagem.query.filter(msg_by = id).filter(msg_to = uid).filter(or_(msg_by=uid).filter(msg_to=id))
#         #orderby
        
#         return render_template('chats.html', chats=chats,)
#     return redirect(url_for('login'))
