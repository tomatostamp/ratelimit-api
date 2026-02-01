from flask import Flask, request, jsonify
from ratelimiter import rate_limit, WINDOW_SECONDS, RATE_LIMIT

app = Flask(__name__)

@app.route("/api/data")
def get_data():
    user_id = request.headers.get("X-User-ID")
    api_name = "/api/data"


    if not user_id:
        return jsonify({"error": "Missing User ID"}), 400
    
    allowed, current_count = rate_limit(user_id, api_name)

    if not allowed:
        return jsonify({"message": f"Rate limit exceeded. Try again in {WINDOW_SECONDS} seconds."}), 429

    return jsonify({"message": f"Request successful. Count for this time window: {current_count}/{RATE_LIMIT}"})

if __name__ == "__main__":
    app.run(debug=True)

