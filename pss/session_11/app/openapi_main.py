import connexion
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from prometheus_client import make_wsgi_app


app = connexion.App(__name__, specification_dir="./")
app.add_api("swagger.yml")  # Add the API definition.

flask_app = app.app  # Get the Flask app instance.
flask_app.wsgi_app = DispatcherMiddleware(flask_app.wsgi_app, 
                                          {"/metrics": make_wsgi_app()})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
