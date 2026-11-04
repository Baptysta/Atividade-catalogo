import sqlite3
from flask import Flask, flash, redirect, render_template, request, url_for

app = Flask(__name__)
app.secret_key = "chave-secreta-catalogo-filmes"

DATABASE = "filmes.db"


def obter_conexao():
  conexao = sqlite3.connect(DATABASE)
  conexao.row_factory = sqlite3.Row
  return conexao


def inicializar_banco():
  conexao = obter_conexao()
  conexao.execute("""
        CREATE TABLE IF NOT EXISTS filmes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            genero TEXT NOT NULL,
            ano INTEGER NOT NULL,
            nota REAL NOT NULL
        )
    """)
  conexao.commit()
  conexao.close()


@app.route("/")
def index():
  conexao = obter_conexao()
  filmes = conexao.execute("SELECT * FROM filmes ORDER BY id DESC").fetchall()
  conexao.close()
  return render_template("index.html", filmes=filmes)


@app.route("/novo", methods=("GET", "POST"))
def novo():
  if request.method == "POST":
    titulo = request.form.get("titulo")
    genero = request.form.get("genero")
    ano = request.form.get("ano")
    nota = request.form.get("nota")

    if not titulo or not genero or not ano or not nota:
      flash("Todos os campos são obrigatórios!", "danger")
    else:
      conexao = obter_conexao()
      conexao.execute(
          "INSERT INTO filmes (titulo, genero, ano, nota) VALUES (?, ?, ?, ?)",
          (titulo, genero, ano, nota),
      )
      conexao.commit()
      conexao.close()
      flash("Filme cadastrado com sucesso!", "success")
      return redirect(url_for("index"))

  return render_template("form.html", acao="Cadastrar Novo Filme", filme=None)


@app.route("/editar/<int:id>", methods=("GET", "POST"))
def editar(id):
  conexao = obter_conexao()
  filme = conexao.execute(
      "SELECT * FROM filmes WHERE id = ?", (id,)
  ).fetchone()

  if request.method == "POST":
    titulo = request.form.get("titulo")
    genero = request.form.get("genero")
    ano = request.form.get("ano")
    nota = request.form.get("nota")

    if not titulo or not genero or not ano or not nota:
      flash("Todos os campos são obrigatórios!", "danger")
    else:
      conexao.execute(
          "UPDATE filmes SET titulo = ?, genero = ?, ano = ?, nota = ? WHERE"
          " id = ?",
          (titulo, genero, ano, nota, id),
      )
      conexao.commit()
      conexao.close()
      flash("Filme atualizado com sucesso!", "success")
      return redirect(url_for("index"))

  conexao.close()
  return render_template("form.html", acao="Editar Filme", filme=filme)


@app.route("/excluir/<int:id>", methods=("POST",))
def excluir(id):
  conexao = obter_conexao()
  conexao.execute("DELETE FROM filmes WHERE id = ?", (id,))
  conexao.commit()
  conexao.close()
  flash("Filme excluído com sucesso!", "success")
  return redirect(url_for("index"))


inicializar_banco()

if __name__ == "__main__":
  app.run(debug=True)