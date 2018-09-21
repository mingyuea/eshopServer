from flask import (
	Blueprint, flash, g, request, jsonify
)

from application.db import get_db

bp = Blueprint('operations', __name__)

@bp.route('/addCart')
def addCart:
	db = get_db()