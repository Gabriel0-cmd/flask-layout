
import os
import sqlite3
from functools import wraps

from flask import Flask, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("FLASK_SECRET_KEY", "chave-local-de-desenvolvimento")
app.config["DATABASE"] = os.path.join(app.root_path, "dados.db")
app.config["DEMO_USERNAME"] = os.environ.get("DEMO_USERNAME", "gabriel")
app.config["DEMO_PASSWORD"] = os.environ.get("DEMO_PASSWORD", "estudo123")


def get_db_connection():
    connection = sqlite3.connect(app.config["DATABASE"])
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    os.makedirs(os.path.dirname(app.config["DATABASE"]), exist_ok=True)
    connection = get_db_connection()
    try:
        connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome_usuario TEXT UNIQUE NOT NULL,
                senha_hash TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS notas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_id INTEGER NOT NULL,
                materia TEXT NOT NULL,
                nota REAL NOT NULL,
                bimestre TEXT NOT NULL,
                FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
            );
            CREATE TABLE IF NOT EXISTS anotacoes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_id INTEGER NOT NULL,
                titulo TEXT NOT NULL,
                conteudo TEXT NOT NULL,
                FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
            );
            """
        )
        usuario = connection.execute(
            "SELECT id FROM usuarios WHERE nome_usuario = ?",
            (app.config["DEMO_USERNAME"],),
        ).fetchone()
        if usuario is None:
            cursor = connection.execute(
                "INSERT INTO usuarios (nome_usuario, senha_hash) VALUES (?, ?)",
                (
                    app.config["DEMO_USERNAME"],
                    generate_password_hash(app.config["DEMO_PASSWORD"]),
                ),
            )
            usuario_id = cursor.lastrowid
            connection.executemany(
                "INSERT INTO notas (usuario_id, materia, nota, bimestre) VALUES (?, ?, ?, ?)",
                [
                    (usuario_id, "Programação", 9.5, "1º bimestre"),
                    (usuario_id, "Banco de dados", 8.8, "1º bimestre"),
                    (usuario_id, "Desenvolvimento web", 9.0, "1º bimestre"),
                ],
            )
            connection.executemany(
                "INSERT INTO anotacoes (usuario_id, titulo, conteudo) VALUES (?, ?, ?)",
                [
                    (usuario_id, "Objetivo", "Continuar aprendendo programação e criar projetos úteis."),
                    (usuario_id, "Próximo passo", "Praticar consultas SQL e desenvolver uma aplicação web."),
                ],
            )
        connection.commit()
    finally:
        connection.close()


@app.before_request
def ensure_database():
    if not app.config.get("DATABASE_INITIALIZED"):
        init_db()
        app.config["DATABASE_INITIALIZED"] = True


def login_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if "usuario_id" not in session:
            return redirect(url_for("login"))
        return view(**kwargs)

    return wrapped_view


@app.route("/")
def index():
    return render_template("index.html", title="Home")


@app.route("/boletim")
@login_required
def boletim():
    connection = get_db_connection()
    try:
        notas = connection.execute(
            "SELECT materia, nota, bimestre FROM notas WHERE usuario_id = ? ORDER BY id",
            (session["usuario_id"],),
        ).fetchall()
    finally:
        connection.close()
    return render_template("boletim.html", title="Boletim", notas=notas)


@app.route("/anotacoes")
@login_required
def anotacoes():
    connection = get_db_connection()
    try:
        registros = connection.execute(
            "SELECT titulo, conteudo FROM anotacoes WHERE usuario_id = ? ORDER BY id",
            (session["usuario_id"],),
        ).fetchall()
    finally:
        connection.close()
    return render_template("anotacoes.html", title="Anotações", registros=registros)


@app.route("/login", methods=["GET", "POST"])
def login():
    erro = None
    if request.method == "POST":
        nome_usuario = request.form.get("nome_usuario", "").strip()
        senha = request.form.get("senha", "")
        connection = get_db_connection()
        try:
            usuario = connection.execute(
                "SELECT id, nome_usuario, senha_hash FROM usuarios WHERE nome_usuario = ?",
                (nome_usuario,),
            ).fetchone()
        finally:
            connection.close()

        if usuario is None or not check_password_hash(usuario["senha_hash"], senha):
            erro = "Usuário ou senha inválidos."
        else:
            session.clear()
            session["usuario_id"] = usuario["id"]
            session["nome_usuario"] = usuario["nome_usuario"]
            return redirect(url_for("boletim"))

    return render_template("login.html", title="Entrar", erro=erro)


@app.route("/sair")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/sobremim", strict_slashes=False)
@app.route("/sobre-mim", strict_slashes=False)
def sobremim():
    return render_template("sobremim.html", title="Sobre mim")


@app.route("/validacao", methods=["GET", "POST"], strict_slashes=False)
def validacao():
    dados = ["", "", ""]
    resultado = []
    erro = None

    if request.method == "POST":
        campos = ["nome", "sobrenome", "idade"]
        indice = 0
        while indice < len(campos):
            dados[indice] = request.form.get(campos[indice], "").strip()
            indice += 1

        try:
            idade = int(dados[2])
            if idade < 0:
                raise ValueError
        except ValueError:
            erro = "Digite uma idade válida, usando um número inteiro maior ou igual a zero."
        else:
            if not dados[0] or not dados[1]:
                erro = "Preencha o nome e o sobrenome."
            else:
                resultado.append(f"Resultado para {dados[0]} {dados[1]}:")
                resultado.append(f"Idade: {idade} anos.")
                resultado.append(
                    "Você pode votar."
                    if idade >= 16
                    else "Você ainda não pode votar."
                )
                resultado.append(
                    "O voto é obrigatório."
                    if idade >= 18
                    else "O voto é facultativo."
                )
                resultado.append(
                    "Você pode dirigir."
                    if idade >= 18
                    else "Você ainda não pode dirigir."
                )

    return render_template(
        "validacao.html",
        title="Validação de idade",
        dados=dados,
        resultado=resultado,
        erro=erro,
    )


if __name__ == "__main__":
    app.run(debug=True)

