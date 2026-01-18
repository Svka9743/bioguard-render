from flask import Flask, request, jsonify
import psycopg2
import os

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

print("Database connected successfully")

@app.route("/block", methods=["POST"])
def block_ip():
    data = request.get_json()

    ip = data.get("meta", {}).get("src")
    score = data.get("score")

    cur.execute(
        "INSERT INTO alerts (ip, score) VALUES (%s, %s)",
        (ip, score)
    )

    conn.commit()

    print("Blocked IP stored:", ip)

    return jsonify({"status": "blocked", "ip": ip})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
