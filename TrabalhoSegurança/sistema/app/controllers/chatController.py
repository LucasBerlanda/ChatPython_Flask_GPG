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
        
        MensagensBanco = db.session.query(Mensagem).from_statement(text("SELECT * FROM mensagem where msg_by=msg_by and msg_to=msg_to or msg_by=msg_to and msg_to=msg_by")).params(msg_by=idLogado, msg_to=idDestinatario).all()
        chatsMensagem = decriptString(MensagensBanco)
        form = MessageForm()
    
        if form.validate_on_submit():
        
            texto = form.body.data
            encr = encriptString(texto)
            msg = Mensagem(body=encr, msg_by=idLogado, msg_to=destinatario.id)
            db.session.add(msg)
            db.session.commit()
        
            MensagensBanco = db.session.query(Mensagem).from_statement(text("SELECT * FROM mensagem where msg_by= msg_by and msg_to=msg_to or msg_by= msg_to and msg_to=msg_by")).params(msg_by=idLogado, msg_to=idDestinatario).all()
            chatsMensagem = decriptString(MensagensBanco)
            return render_template("chat.html", form=form, destinatario=destinatario, chatsMensagem=chatsMensagem)
    
        return render_template("chat.html", form=form, destinatario=destinatario, chatsMensagem=chatsMensagem)


    
def encriptString(msg):
    gpg = gnupg.GPG()
    unencrypted_string = msg
    encrypted_data = gpg.encrypt(unencrypted_string, 'lucas@gmail.com')
    encrypted_string = str(encrypted_data)

    return encrypted_string
    
def decriptString(objeto):
    gpg = gnupg.GPG()
    
    msgTela = []
    
    for msg in objeto:
        unencrypted_string = msg.body
        decrypted_data = gpg.decrypt(unencrypted_string, passphrase='minhasenha')
        texto = decrypted_data
        msgTela.append(Mensagem(texto, msg.msg_by , msg.msg_to))
    
    return msgTela
