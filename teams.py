import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from app.db import get_db

bp = Blueprint('teams', __name__, url_prefix='/teams')


@bp.route('/', methods=('GET', 'POST'))
def createTeam():
    print("inside createTeam")
    teams = []
    db = get_db()
    print(request.form)
    if "teamName" in request.form:
        if request.method == 'POST':
            team = request.form['teamName']
            error = None

            if not team:
                error = 'Team name cannot be blank.'

            if error is None:
                db.execute(
                    'INSERT INTO teams (name) VALUES (?)',
                    (team,)
                )
                db.commit()

    elif "message" in request.form:
        if request.method == 'POST':
            teamID = request.form['teamID']
            message = request.form['message']
            error = None

            if not message:
                error = 'Team name cannot be blank.'

            if error is None:
                db.execute(
                    'INSERT INTO posts (message, team_id) VALUES (?,?)',
                    (message,teamID,)
                )
                db.commit()
        #print("postMessage form")


    teamQuery = db.execute('SELECT * FROM teams')
    teamRows = teamQuery.fetchall()
    for row in teamRows:
        teams.append((row['id'], row['name']))


    return render_template('teams/index.html', items = teams)

