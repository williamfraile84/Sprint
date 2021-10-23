from flask import Flask
from flask_jsglue import JSGlue
import hashlib
import os
app = Flask(__name__)

jsglue = JSGlue(app)


app.secret_key = os.urandom(24)
from app import rutas


