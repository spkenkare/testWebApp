import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from app.db import get_db


bp = Blueprint('badimage', __name__, url_prefix='/badimage')

@bp.route('/') #at the index
def displayImage(): 
    return render_template('image/index.html')
