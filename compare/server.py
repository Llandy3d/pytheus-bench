import os
from flask import Flask, Response, request
from flask_sqlalchemy import SQLAlchemy
from pytheus.metrics import Counter, Histogram
from pytheus.exposition import generate_metrics, PROMETHEUS_CONTENT_TYPE


if os.environ.get('PYTHEUS_MULTIPROCESS_TEST'):
    from pytheus.backends import load_backend
    from pytheus.backends.redis import MultiProcessRedisBackend

    load_backend(
        backend_class=MultiProcessRedisBackend,
        backend_config={"host": "redis", "port": 6379},
    )


workers_count = os.environ.get('WORKERS_COUNT')
assert workers_count


http_hit_count_total = Counter(
    'http_hit_count_total',
    'description',
    required_labels=['workers_count'],
    default_labels={'workers_count': workers_count}
)

http_request_duration_seconds = Histogram(
    'http_request_duration_seconds',
    'description',
)


app = Flask(__name__)
db = SQLAlchemy()
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
db.init_app(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=False, nullable=False)
    email = db.Column(db.String)


with app.app_context():
    db.create_all()


@app.route("/users/create", methods=["POST"])
@http_request_duration_seconds
def user_create():
    data = request.json
    user = User(
        username=data["username"],
        email=data["email"],
    )
    db.session.add(user)
    db.session.commit()
    return Response()


@app.route("/metrics")
def metrics():
    data = generate_metrics()
    return Response(data, headers={'Content-Type': PROMETHEUS_CONTENT_TYPE})


@app.route("/")
@http_request_duration_seconds
def hello_world():
    http_hit_count_total.inc()
    return "<p>Hello, World!</p>"
