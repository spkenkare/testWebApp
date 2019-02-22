import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from app.db import get_db

bp = Blueprint('teams', __name__, url_prefix='/teams')


@bp.route('/') #at the index
def displayTeams(): #display all teams
    teams = []
    db = get_db()
    teamQuery = db.execute('SELECT * FROM teams')
    teamRows = teamQuery.fetchall()
    for row in teamRows:
        teams.append((row['id'], row['name']))
    return render_template('teams/index.html', teamIDs = teams)
    
@bp.route('/', methods=('GET', 'POST'))
def createTeam(): #offer option to create new teams
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

    """
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
    """
    """
    teamQuery = db.execute('SELECT id FROM teams')
    teamRows = teamQuery.fetchall()
    for row in teamRows:
        #messagesQuery = db.execute('SELECT message FROM posts WHERE team_id = ?', (row['id'],))
        #messageRows = messagesQuery.fetchall()
        #messages = []
        #for mRow in messageRows:
        #    messages.append(mRow['message'])
        #teams.append((row['id'], row['name'], messages))
        teams.append(row['id'])

    return render_template('teams/index.html', teamIDs = teams)
    """
    return displayTeams()

@bp.route('/messages.html/<teamID>', subdomain = '<teamName>') #for each iframe/team page
def returnMessages(teamID, teamName): #display the current messages
    db = get_db()
    print("Team ID: ", teamID)
    nameQuery = db.execute('SELECT name FROM teams WHERE id = ?', (teamID,))
    nameRows = nameQuery.fetchall()
    name = nameRows[0]['name']
    print(name)
    messagesQuery = db.execute('SELECT message FROM posts WHERE team_id = ?', (teamID,))
    messageRows = messagesQuery.fetchall()
    messages = []
    for mRow in messageRows:
        messages.append(mRow['message'])
    return render_template('teams/messages.html', messages = messages, name = name)

@bp.route('/messages.html/<teamID>', methods=('GET', 'POST'))
def postMessage(teamID): #when someone posts a message to a team
    db = get_db()
    if request.method == 'POST':
        message = request.form['message']
        error = None

        if not message:
            error = 'Message cannot be blank.'

        if error is None:
            db.execute(
                'INSERT INTO posts (message, team_id) VALUES (?,?)',
                (message,teamID,)
            )
            db.commit()

    nameQuery = db.execute('SELECT name FROM teams WHERE id = ?', (teamID,))
    nameRows = nameQuery.fetchall()
    name = nameRows[0]['name']
    return returnMessages(teamID, name)
