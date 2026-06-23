from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    aluno = {
        "nome": "Pedro",
        "turma": "2°EM Tecnico"
    }
    professores =[
        {
            "nome": "Ishara",
            "materia": "Web"
        },
            {
                "nome": "Edidio",
                "materia": "Software"
            }
    ]
    return render_template('index.html', title="Home", aluno=aluno)

@app.route("/boletim")
def boletim():
    return render_template('boletim.html', title="Boletim")
