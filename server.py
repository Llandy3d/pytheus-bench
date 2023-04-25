import os
from flask import Flask, Response
from pytheus.metrics import Counter
from pytheus.exposition import generate_metrics, PROMETHEUS_CONTENT_TYPE


if os.environ.get('PYTHEUS_MULTIPROCESS_TEST'):
    from pytheus.backends import load_backend
    from pytheus.backends.redis import MultiProcessRedisBackend

    load_backend(
        backend_class=MultiProcessRedisBackend,
        backend_config={"host": "redis", "port": 6379},
    )


http_hit_count_total = Counter('http_hit_count_total', 'description')


app = Flask(__name__)


@app.route("/metrics")
def metrics():
    data = generate_metrics()
    return Response(data, headers={'Content-Type': PROMETHEUS_CONTENT_TYPE})


@app.route("/")
def hello_world():
    http_hit_count_total.inc()
    return "<p>Hello, World!</p>"
