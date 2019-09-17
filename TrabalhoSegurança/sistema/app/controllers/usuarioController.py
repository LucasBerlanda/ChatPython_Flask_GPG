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
        flash('Parabéns, cadastro realizado com sucesso!')
        return redirect(url_for('index'))
    return render_template('usuario/registrar.html', title='Register', form=form)

@app.route("/listaUsuarios")
@login_required
def listaUsuarios():
    usuarios = Usuario.query.all()
    
    return render_template("usuario/lista.html", usuarios = usuarios)

@app.route("/editarUsuario/<int:id>", methods=['GET', 'POST'])
@login_required
def editarUsuario(id):
        usuario = Usuario.query.filter_by(id = id).first()
        perfisAcesso = PerfilAcesso.query.all()
        setores = Setor.query.all()
        
        if request.method == "POST":
                username = (request.form.get("username"))
                setor_id = (request.form.get("setor_id"))
                perfilAcesso_id = (request.form.get("perfilAcesso_id"))
                
                if username and setor_id and perfilAcesso_id:
                        usuario.username = username
                        usuario.setor_id = setor_id
                        usuario.perfilAcesso_id = perfilAcesso_id
                        
                        db.session.commit()
                        db.session.close()
                        
                        return redirect(url_for("listaUsuarios"))
        
        return render_template("usuario/editar.html", usuario = usuario, perfisAcesso = perfisAcesso, setores = setores)


@app.route("/excluirUsuario/<int:id>")
@login_required
def excluirUsuario(id):
    usuario = Usuario.query.filter_by(id = _id).first()
      
    db.session.delete(usuario)
    db.session.commit()
    
    usuarios = Usuario.query.all()
    
    return render_template("setor/lista.html", usuarios = usuarios)