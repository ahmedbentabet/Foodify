#!/usr/bin/env python3
"""The Foodify app
"""
from flask import Flask
<<<<<<< HEAD
from views import app_views


foodify_app: Flask = Flask(__name__)
foodify_app.register_blueprint(app_views)


if __name__ == "__main__":
    foodify_app.run(debug=True)
=======
from routes import app_blueprint

foodify_app: Flask = Flask(__name__)
foodify_app.register_blueprint(app_blueprint)


if __name__ == "__main__":
    foodify_app.run(debug=True)
>>>>>>> origin/Ahmed_Branch
