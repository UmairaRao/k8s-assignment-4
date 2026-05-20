import os
from flask import Flask, request, redirect, render_template_string
import mysql.connector

app = Flask(__name__)

DB_HOST = os.getenv("DB_HOST", "mysql-service")
DB_PORT = int(os.getenv("DB_PORT", "3306"))
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "rootpass")
DB_NAME = os.getenv("DB_NAME", "messagesdb")


def get_connection():
    return mysql.connector.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
    )


def init_db():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS messages (
            id INT AUTO_INCREMENT PRIMARY KEY,
            content VARCHAR(255) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    conn.commit()
    cur.close()
    conn.close()


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        message = request.form.get("message", "").strip()
        if message:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("INSERT INTO messages (content) VALUES (%s)", (message,))
            conn.commit()
            cur.close()
            conn.close()
        return redirect("/")

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, content, created_at FROM messages ORDER BY id DESC")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    return render_template_string(
        """
        <!doctype html>
        <html>
        <head><title>Flask MySQL Messages</title></head>
        <body>
            <h1>Flask + MySQL Message Board</h1>
            <form method="post">
                <input type="text" name="message" placeholder="Enter message" required>
                <button type="submit">Save</button>
            </form>
            <h2>Saved Messages</h2>
            <ul>
                {% for row in rows %}
                  <li><b>#{{ row[0] }}</b> - {{ row[1] }} ({{ row[2] }})</li>
                {% else %}
                  <li>No messages yet.</li>
                {% endfor %}
            </ul>
        </body>
        </html>
        """,
        rows=rows,
    )


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)
