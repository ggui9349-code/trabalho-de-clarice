from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from pathlib import Path

app = Flask(__name__)
app.secret_key = "senai-mini-app-tarefas"

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "tarefas.db"


def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_connection()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS tarefas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            descricao TEXT,
            status TEXT NOT NULL DEFAULT 'Pendente'
                CHECK(status IN ('Pendente', 'Concluída')),
            criada_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    conn.commit()
    conn.close()


@app.route("/")
def index():
    filtro = request.args.get("status", "Todas")
    conn = get_db_connection()

    if filtro in ("Pendente", "Concluída"):
        tarefas = conn.execute(
            "SELECT * FROM tarefas WHERE status = ? ORDER BY id DESC", (filtro,)
        ).fetchall()
    else:
        filtro = "Todas"
        tarefas = conn.execute("SELECT * FROM tarefas ORDER BY id DESC").fetchall()

    conn.close()
    return render_template("index.html", tarefas=tarefas, filtro=filtro)


@app.route("/adicionar", methods=["POST"])
def adicionar():
    titulo = request.form.get("titulo", "").strip()
    descricao = request.form.get("descricao", "").strip()

    if not titulo:
        flash("Informe um título para a tarefa.", "erro")
        return redirect(url_for("index"))

    conn = get_db_connection()
    conn.execute(
        "INSERT INTO tarefas (titulo, descricao, status) VALUES (?, ?, ?)",
        (titulo, descricao, "Pendente"),
    )
    conn.commit()
    conn.close()

    flash("Tarefa cadastrada com sucesso!", "sucesso")
    return redirect(url_for("index"))


@app.route("/status/<int:id>", methods=["POST"])
def alterar_status(id):
    conn = get_db_connection()
    tarefa = conn.execute("SELECT * FROM tarefas WHERE id = ?", (id,)).fetchone()

    if tarefa is None:
        conn.close()
        flash("Tarefa não encontrada.", "erro")
        return redirect(url_for("index"))

    novo_status = "Concluída" if tarefa["status"] == "Pendente" else "Pendente"
    conn.execute("UPDATE tarefas SET status = ? WHERE id = ?", (novo_status, id))
    conn.commit()
    conn.close()

    flash(f"Status alterado para {novo_status}.", "sucesso")
    return redirect(request.referrer or url_for("index"))


@app.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    conn = get_db_connection()
    tarefa = conn.execute("SELECT * FROM tarefas WHERE id = ?", (id,)).fetchone()

    if tarefa is None:
        conn.close()
        flash("Tarefa não encontrada.", "erro")
        return redirect(url_for("index"))

    if request.method == "POST":
        titulo = request.form.get("titulo", "").strip()
        descricao = request.form.get("descricao", "").strip()
        status = request.form.get("status", "Pendente")

        if not titulo:
            conn.close()
            flash("O título da tarefa não pode ficar vazio.", "erro")
            return redirect(url_for("editar", id=id))

        if status not in ("Pendente", "Concluída"):
            status = "Pendente"

        conn.execute(
            "UPDATE tarefas SET titulo = ?, descricao = ?, status = ? WHERE id = ?",
            (titulo, descricao, status, id),
        )
        conn.commit()
        conn.close()

        flash("Tarefa atualizada com sucesso!", "sucesso")
        return redirect(url_for("index"))

    conn.close()
    return render_template("editar.html", tarefa=tarefa)


@app.route("/excluir/<int:id>", methods=["POST"])
def excluir(id):
    conn = get_db_connection()
    tarefa = conn.execute("SELECT id FROM tarefas WHERE id = ?", (id,)).fetchone()

    if tarefa is None:
        conn.close()
        flash("Tarefa não encontrada.", "erro")
        return redirect(url_for("index"))

    conn.execute("DELETE FROM tarefas WHERE id = ?", (id,))
    conn.commit()
    conn.close()

    flash("Tarefa excluída com sucesso!", "sucesso")
    return redirect(request.referrer or url_for("index"))


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
