import prometheus_client
from flask import Flask
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from app.helpers.middleware import setup_metrics


def index():
    return 'home'


def cpu():  # this is to mimic a spike in CPU
    # for older machines, lower the range to prevent timeouts
    for i in range(10**4):
        i**i

    return 'cpu intensive operation complete'


def memory():  # this is to mimic a spike in memory usage
    d = {}
    # for older machines, lower the range to prevent timeouts
    for i in range(10**7):
        i = str(i)
        i += "xyz"
        d[i] = i

    return 'memory intensive operation complete'


def create_app():
    main_app = Flask(__name__)
    main_app.add_url_rule('/', 'index', index)
    main_app.add_url_rule('/cpu', 'cpu', cpu)
    main_app.add_url_rule('/memory', 'memory', memory)
    setup_metrics(main_app)

    # Add prometheus wsgi middleware to route /metrics requests
    # this middleware allows us to distinguish between our Flask wsgi app and prometheus wsgi app
    # read more here: https://flask.palletsprojects.com/en/2.2.x/patterns/appdispatch/
    app = DispatcherMiddleware(
        app=main_app.wsgi_app,
        mounts={'/metrics': prometheus_client.make_wsgi_app()}
    )

    return app
