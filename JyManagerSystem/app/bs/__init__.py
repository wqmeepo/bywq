from flask import Blueprint

bs = Blueprint('bs', __name__)

import app.bs.views
