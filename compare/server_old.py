import os
import prometheus_client
from flask import Flask, Response
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST, REGISTRY


# remove platform collectors
prometheus_client.REGISTRY.unregister(prometheus_client.GC_COLLECTOR)
prometheus_client.REGISTRY.unregister(prometheus_client.PLATFORM_COLLECTOR)
prometheus_client.REGISTRY.unregister(prometheus_client.PROCESS_COLLECTOR)


registry = REGISTRY
if os.environ.get('PROMETHEUS_MULTIPROC_DIR'):
    registry = prometheus_client.CollectorRegistry()
    prometheus_client.multiprocess.MultiProcessCollector(registry)


http_hit_count_total = Counter(
    'http_hit_count_total',
    'description',
    labelnames=['workers_count'],
    registry=registry,
)
http_hit_count_total_labeled = http_hit_count_total.labels('1')

http_request_duration_seconds = Histogram(
    'http_request_duration_seconds',
    'description',
    registry=registry,
)


app = Flask(__name__)


@app.route("/metrics")
def metrics():
    data = generate_latest(registry)
    return Response(data, headers={'Content-Type': CONTENT_TYPE_LATEST})


@app.route("/")
@http_request_duration_seconds.time()
def hello_world():
    http_hit_count_total_labeled.inc()
    return "<p>Hello, World!</p>"
