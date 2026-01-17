import os
import psycopg2
from flask import Flask, request, jsonify

app = Flask(__name__)

# Read database URL from Render environment
DB_URL = os.getenv("DATABASE_URL")

conn = None
cur = None

# Safe database connection
try:
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

except Exception as e:
    print("Database connection failed:", e)

# API endpoint
@app.route("/block", methods=["POST"])
def block():
    data = request.get_json()
    ip = data.get("source", {}).get("src")
    score = data.get("score")

    if cur:
        cur.execute("INSERT INTO alerts (ip, score) VALUES (%s, %s)", (ip, score))
        conn.commit()

    return jsonify({"status": "stored", "ip": ip})

# IMPORTANT: Start Flask server on Render PORT
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
