from flask import render_template, url_for, redirect, request, flash 
from app import app, db
from app.forms import LoginForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import Usuario, Mensagem
from werkzeug.urls import url_parse
from app.forms import MessageForm
from sqlalchemy import text, select, or_, and_
import gnupg
import shutil
import os

@app.route('/chat/<int:id>', methods=['GET', 'POST'])
def chat(id):
    
    destinatario = Usuario.query.filter_by(id = id).first()    
    idLogado = current_user.id
    idDestinatario = destinatario.id

    if destinatario:
        #pega as mensagens do banco decripta e joga pra tela
        MensagensBanco = db.session.query(Mensagem).from_statement(text("SELECT * FROM mensagem where msg_by=msg_by and msg_to=msg_to or msg_by=msg_to and msg_to=msg_by")).params(msg_by=idLogado, msg_to=idDestinatario).all()
        chatsMensagem = decriptString(MensagensBanco)
        # form = MessageForm()
    
        if request.method == "POST":
            #pega msg
            texto = (request.form.get("msg"))
            
            # faz o encript chamando o metodo
            encr = encriptString(texto)
            #seta os valores para inserir no banco
            msg = Mensagem(body=encr, msg_by=idLogado, msg_to=destinatario.id)
            db.session.add(msg)
            db.session.commit()
        
            #pega as mensagens do banco e em seguida faz o decript e joga pra tela
            MensagensBanco = db.session.query(Mensagem).from_statement(text("SELECT * FROM mensagem where msg_by=msg_by and msg_to=msg_to or msg_by= msg_to and msg_to=msg_by")).params(msg_by=idLogado, msg_to=idDestinatario).all()
            chatsMensagem = decriptString(MensagensBanco)
            
            return render_template("chat.html", destinatario=destinatario, chatsMensagem=chatsMensagem)
    
        return render_template("chat.html", destinatario=destinatario, chatsMensagem=chatsMensagem)


    
def encriptString(msg):
    gpg = gnupg.GPG()
    unencrypted_string = msg
    encrypted_data = gpg.encrypt(unencrypted_string, 'lucas@gmail.com')
    encrypted_string = str(encrypted_data)

    return encrypted_string
    
def decriptString(objetoMsg):
    gpg = gnupg.GPG()
    
    msgTela = []
    
    for msg in objetoMsg:
        #unencrypted_string = msg.body
        decrypted_data = gpg.decrypt(msg.body, passphrase='minhasenha')

        msgTela.append(Mensagem(decrypted_data, msg.msg_by , msg.msg_to))
    
    return msgTela
