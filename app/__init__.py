import os

from flask import Flask

app = Flask(__name__)

app.config.from_object(os.environ['CONFIG_CLASS'])

from app.views.login import LoginView
LoginView.register(app)

from app.views.constituent import ConstituentView
ConstituentView.register(app)