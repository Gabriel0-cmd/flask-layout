
from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html", title="Home")


@app.route("/boletim")
def boletim():
    return render_template("boletim.html", title="Boletim")


@app.route("/sobremim")
def sobremim():
    return render_template("sobremim.html", title="Sobre mim")


if __name__ == "__main__":
    app.run(debug=True)

