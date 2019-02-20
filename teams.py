import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from app.db import get_db

bp = Blueprint('teams', __name__, url_prefix='/teams')


@bp.route('/', methods=('GET', 'POST'))
def createAndDisplayTeams():
    teams = []
    db = get_db()
    if request.method == 'POST':
        team = request.form['teamName']
        #teams.append(team)
        error = None

        if not team:
            error = 'Team name cannot be blank.'

        if error is None:
            db.execute(
                'INSERT INTO teams (name) VALUES (?)',
                (team,)
            )
            db.commit()

    teamQuery = db.execute('SELECT name FROM teams')
    teamRows = teamQuery.fetchall()
    for row in teamRows:
        teams.append(row['name'])


    return render_template('teams/index.html', items = teams)

