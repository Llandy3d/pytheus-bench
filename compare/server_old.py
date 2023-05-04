import os
from flask import Flask, Response
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST


http_hit_count_total = Counter(
    'http_hit_count_total',
    'description',
    labelnames=['workers_count'],
)

http_request_duration_seconds = Histogram(
    'http_request_duration_seconds',
    'description',
)


app = Flask(__name__)


@app.route("/metrics")
def metrics():
    data = generate_latest()
    return Response(data, headers={'Content-Type': CONTENT_TYPE_LATEST})


@app.route("/")
@http_request_duration_seconds.time()
def hello_world():
    http_hit_count_total.labels('1').inc()
    return "<p>Hello, World!</p>"
