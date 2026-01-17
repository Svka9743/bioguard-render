import os
import psycopg2
from flask import Flask, request, jsonify

app = Flask(__name__)
DB_URL = os.getenv("DATABASE_URL")

conn = psycopg2.connect(DB_URL)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS alerts (
    id SERIAL PRIMARY KEY,
    ip TEXT,
    score FLOAT,
    time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")
conn.commit()

@app.route("/block", methods=["POST"])
def block():
    data = request.get_json()
    ip = data.get("source", {}).get("src")
    score = data.get("score")

    cur.execute("INSERT INTO alerts (ip, score) VALUES (%s, %s)", (ip, score))
    conn.commit()

    return jsonify({"status": "stored", "ip": ip})
