from flask import render_template, url_for, redirect, request, flash  
from app import app, db
from app.models import Usuario
from sqlalchemy import text
from app.forms import RegistraUsuarioForm
from flask_login import current_user, login_user, logout_user, login_required

@app.route('/cadastroUsuario', methods=['GET', 'POST'])

def cadastroUsuario():

    form = RegistraUsuarioForm()
    
    if form.validate_on_submit():
        user = Usuario(name=form.name.data, email=form.email.data, username=form.username.data, password_hash=form.password.data, status=False)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Parabéns, cadastro realizado com sucesso!', 'info')
        return redirect(url_for('index'))
    return render_template('usuario/registrar.html', title='Register', form=form)

@app.route("/listaUsuarios")
@login_required
def listaUsuarios():
    usuarios = Usuario.query.all()
    
    return render_template("usuario/lista.html", usuarios = usuarios)

