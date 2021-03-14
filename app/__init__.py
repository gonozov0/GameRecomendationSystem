from flask import Flask

app = Flask(__name__)

from app.model import Model

model = Model()

from app import routes