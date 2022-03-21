from flask import Blueprint

workspace = Blueprint('workspace', __name__)

import app.workspace.views
