from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/block", methods=["POST"])
def block():
    data = request.get_json()
    src = data.get("source", {})
    ip = src.get("src")
    score = data.get("score")

    if not ip:
        return jsonify({"error":"no ip"}), 400

    # For testing: append blocked IP to a file
    with open("blocked_ips.log", "a") as f:
        f.write(f"{ip},{score}\n")

    return jsonify({"status":"logged","ip":ip})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9000)
