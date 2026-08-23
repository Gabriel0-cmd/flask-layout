
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html", title="Home")


@app.route("/boletim")
def boletim():
    return render_template("boletim.html", title="Boletim")


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

