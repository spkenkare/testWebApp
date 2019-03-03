import functools

from flask import (
    Blueprint, flash, g, redirect, make_response, render_template, request, session, url_for
)

from app.db import get_db


bp = Blueprint('image', __name__, url_prefix='/image')

@bp.route('/') #at the index
def displayImage(): 
    resp = make_response(render_template('image/index.html'))
    resp.headers['Content-Security-Policy'] = "default-src 'self' *.lvh.me"
    return resp
