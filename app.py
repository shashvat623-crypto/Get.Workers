from flask import Flask, render_template, request, redirect
import sqlite3
import os

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "static/uploads"

def init_db():
    conn = sqlite3.connect("workers.db")
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS workers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            skill TEXT,
            area TEXT,
            phone TEXT,
            photo TEXT
        )
    """)

    conn.commit()
    conn.close()

@app.route("/", methods=["GET", "POST"])
def home():
    conn = sqlite3.connect("workers.db")
    c = conn.cursor()

    if request.method == "POST":
        name = request.form["name"]
        skill = request.form["skill"]
        area = request.form["area"]
        phone = request.form["phone"]

        file = request.files["photo"]
        filename = file.filename
        file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

        c.execute(
            "INSERT INTO workers (name, skill, area, phone, photo) VALUES (?, ?, ?, ?, ?)",
            (name, skill, area, phone, filename)
        )

        conn.commit()
        conn.close()

        return redirect("/")

    search = request.args.get("search")

    if search:
        c.execute(
            "SELECT name, skill, area, phone, photo FROM workers WHERE skill LIKE ?",
            ('%' + search + '%',)
        )
    else:
        c.execute("SELECT name, skill, area, phone, photo FROM workers")

    workers = c.fetchall()

    conn.close()

    return render_template("index.html", workers=workers)

if __name__ == "__main__":
    init_db()
    app.run(debug=True)