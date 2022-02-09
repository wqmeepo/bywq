from flask import Blueprint

businsystem = Blueprint('businsystem', __name__)

import app.businsystem.views
