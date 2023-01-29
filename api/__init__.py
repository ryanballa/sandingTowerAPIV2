import os
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
CORS(app)

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS')
app.config["debug"] = os.getenv('DEBUG')

db = SQLAlchemy(app)
migrate = Migrate(app, db)

@app.route('/')
def hello():
    return 'Hello World'