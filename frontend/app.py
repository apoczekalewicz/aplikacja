import os
import time
import psycopg2
from flask import Flask, render_template_string

app = Flask(__name__)

DB_HOST = os.environ.get("DB_HOST", "db")
DB_PORT = os.environ.get("DB_PORT", "5432")
DB_NAME = os.environ.get("DB_NAME", "appdb")
DB_USER = os.environ.get("DB_USER", "appuser")
DB_PASS = os.environ.get("DB_PASS", "apppass")

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Aplikacja - Counter</title>
    <style>
        body { font-family: Arial, sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; background: #1a1a2e; color: #eee; }
        .card { background: #16213e; padding: 40px 60px; border-radius: 12px; text-align: center; box-shadow: 0 4px 20px rgba(0,0,0,0.3); }
        h1 { color: #e94560; margin-bottom: 10px; }
        .counter { font-size: 72px; font-weight: bold; color: #0f3460; margin: 20px 0; }
        .info { color: #888; font-size: 14px; }
    </style>
</head>
<body>
    <div class="card">
        <h1>Aplikacja</h1>
        <p>Odświeżenia strony:</p>
        <div class="counter">{{ counter }}</div>
        <p class="info">Hostname: {{ hostname }}</p>
        <p class="info">Odśwież stronę aby zwiększyć counter</p>
    </div>
</body>
</html>
"""

def get_db():
    return psycopg2.connect(host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASS)

def init_db():
    for attempt in range(30):
        try:
            conn = get_db()
            cur = conn.cursor()
            cur.execute("CREATE TABLE IF NOT EXISTS counter (id SERIAL PRIMARY KEY, value INTEGER NOT NULL DEFAULT 0)")
            cur.execute("INSERT INTO counter (id, value) VALUES (1, 0) ON CONFLICT (id) DO NOTHING")
            conn.commit()
            cur.close()
            conn.close()
            print("Database initialized successfully")
            return
        except Exception as e:
            print(f"Waiting for database (attempt {attempt+1}/30): {e}")
            time.sleep(2)
    print("WARNING: Could not initialize database, will retry on first request")

@app.route("/")
def index():
    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute("UPDATE counter SET value = value + 1 WHERE id = 1 RETURNING value")
        counter = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
    except Exception:
        try:
            init_db()
            conn = get_db()
            cur = conn.cursor()
            cur.execute("UPDATE counter SET value = value + 1 WHERE id = 1 RETURNING value")
            counter = cur.fetchone()[0]
            conn.commit()
            cur.close()
            conn.close()
        except Exception:
            counter = "ERR"
    hostname = os.environ.get("HOSTNAME", "unknown")
    return render_template_string(HTML, counter=counter, hostname=hostname)

@app.route("/health")
def health():
    return "OK", 200

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=8080)
