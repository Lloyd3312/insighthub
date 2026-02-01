from flask import Flask, jsonify
import random
from prometheus_client import Counter, generate_latest

app = Flask(__name__)

# Prometheus metric
REQUEST_COUNT = Counter(
    'insighthub_requests_total',
    'Total number of requests',
    ['method', 'endpoint']
)

QUOTES = [
    "Discipline beats motivation.",
    "Consistency builds mastery.",
    "Small steps every day.",
    "DevOps is a mindset, not a tool."
]

@app.before_request
def before_request():
    # Track every request
    from flask import request
    REQUEST_COUNT.labels(
        method=request.method,
        endpoint=request.path
    ).inc()

@app.route("/health")
def health():
    return jsonify(status="ok")

@app.route("/quote")
def quote():
    return jsonify(quote=random.choice(QUOTES))

@app.route("/weather")
def weather():
    # Mock data for now (real API later)
    return jsonify(
        city="Istanbul",
        temperature="25°C",
        condition="Sunny"
    )

@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {"Content-Type": "text/plain"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
