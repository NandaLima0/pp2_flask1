import os
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "comidadatabase.db"))
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
db = SQLAlchemy(app)

class Comida(db.Model):
    titulo = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)

    def __repr__(self):
        return "<Título: {}>".format(self.titulo)

@app.route('/', methods=["GET", "POST"])
def home():
    if request.method == "POST":
        try:
            comida = Comida(titulo=request.form.get("title"))
            db.session.add(comida)
            db.session.commit()
        except Exception as e:
            print("Falha ao adicionar a comida:", e)

    comidas = Comida.query.all()
    return render_template("index.html", comidas=comidas)

@app.route("/update", methods=["GET", "POST"])
def update():
    comidas = Comida.query.all()
    if request.method == "POST":
        try:
            titulo_antigo = request.form.get("oldtitle")
            novo_titulo = request.form.get("newtitle")
            comida = Comida.query.filter_by(titulo=titulo_antigo).first()
            if comida:
                comida.titulo = novo_titulo
                db.session.commit()
                mensagem = "O título da comida foi atualizado com sucesso!"
            else:
                mensagem = "Comida não encontrada."
        except Exception as e:
            print("Erro ao atualizar o título da comida:", e)
            mensagem = "Erro ao atualizar a comida."
        return render_template("update.html", comidas=comidas, mensagem=mensagem)

    return render_template("update.html", comidas=comidas)

@app.route("/delete", methods=["GET", "POST"])
def delete():
    comidas = Comida.query.all()
    if request.method == "POST":
        titulo = request.form.get("title")
        comida = Comida.query.filter_by(titulo=titulo).first()
        
        if comida:
            db.session.delete(comida)
            db.session.commit()
            mensagem = "A comida foi deletada com sucesso!"
        else:
            mensagem = "Comida não encontrada."
        
        return render_template("delete.html", comidas=comidas, mensagem=mensagem)

    return render_template("delete.html", comidas=comidas)

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
