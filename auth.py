import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from app.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

messages = []

@bp.route('/addMessage', methods=('GET', 'POST'))
def addMessage():
    if request.method == 'POST':
        message = request.form['message']
        messages.append(message)
        db = get_db()
        error = None

        if not message:
            error = 'Message cannot be blank.'

        if error is None:
            db.execute(
                'INSERT INTO posts (message) VALUES (?)',
                (message,)
            )
            db.commit()

    return render_template('auth/addMessage.html', items = messages)

