from flask import Flask
from flask_bootstrap import Bootstrap




# Declare and configure application
bootstrap = Bootstrap()
app = Flask(__name__, static_url_path='/static')
app.config.from_pyfile('local_settings.py')
bootstrap.init_app(app)
from clicktocall.main import main as main_blueprint
app.register_blueprint(main_blueprint)

