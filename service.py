import time
import os
from flask import Flask, jsonify, request
import redis

# Toggle caching with environment variable: USE_CACHE=1 or 0
USE_CACHE = os.environ.get("USE_CACHE", "1") == "1"

# Connect to Redis (default localhost:6379)
r = redis.Redis(host="localhost", port=6379, db=0)

app = Flask(__name__)

def expensive_operation(key: str) -> str:
    """
    Simulate a slow operation (e.g., heavy DB query or computation).
    """
    time.sleep(1.0)  # 1 second delay
    return f"Expensive result for {key}"

@app.route("/data")
def get_data():
    """
    Endpoint: /data?key=<some_key>
    """
    key = request.args.get("key", "default")

    if USE_CACHE:
        # 1) Try Redis first
        cached = r.get(key)
        if cached is not None:
            return jsonify({
                "source": "cache",
                "key": key,
                "value": cached.decode("utf-8")
            })

    # 2) Cache miss OR cache disabled: do expensive work
    value = expensive_operation(key)

    if USE_CACHE:
        # Store in Redis with 60-second TTL
        r.setex(key, 60, value)

    return jsonify({
        "source": "expensive_operation",
        "key": key,
        "value": value
    })


if __name__ == "__main__":
    # Run Flask app (you can also use gunicorn for more realism)
    app.run(host="0.0.0.0", port=5000, debug=False)