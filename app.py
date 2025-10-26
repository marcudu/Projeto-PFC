from flask import Flask, render_template, redirect, url_for, request, session

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta_aqui'  
USUARIO_FIXO = {'usuario': 'admin', 'senha': '1234'}

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = request.form.get("usuario")
        senha = request.form.get("senha")
        if usuario == USUARIO_FIXO['usuario'] and senha == USUARIO_FIXO['senha']:
            session['usuario'] = usuario
            return redirect(url_for('dashboard'))
        else:
            return render_template("login.html", erro="Usuário ou senha inválidos")
    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    return render_template("dashboard.html", usuario=session['usuario'])

@app.route("/logout")
def logout():
    session.pop('usuario', None)
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)
