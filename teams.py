import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from app.db import get_db


bp = Blueprint('teams', __name__, url_prefix='/teams')

@bp.route('/') #at the index
def displayTeams(): #display all teams
    print("displayTeams")
    teams = []
    db = get_db()
    teamQuery = db.execute('SELECT * FROM teams')
    teamRows = teamQuery.fetchall()
    for row in teamRows:
        teams.append((row['id'], row['name']))
    return render_template('teams/index.html', teamIDs = teams)
    
@bp.route('/', methods=('GET', 'POST'))
def createTeam(): #offer option to create new teams
    print("createTeam")
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

    return displayTeams()


@bp.route('/messages.html', subdomain = '<teamName>') #for each iframe/team page
def returnMessages(teamName): #display the current messages
    print("returnMessages") 
    db = get_db()
    idQuery = db.execute('SELECT id FROM teams WHERE name = ?', (teamName,))
    idRows = idQuery.fetchall()
    teamID = idRows[0]['id']
    messagesQuery = db.execute('SELECT message FROM posts WHERE team_id = ?', (teamID,))
    messageRows = messagesQuery.fetchall()
    messages = []
    for mRow in messageRows:
        messages.append(mRow['message'])
    return render_template('teams/messages.html', messages = messages, name = teamName)

    #return render_template('teams/messages.html', name = teamName)


@bp.route('/messages.html', subdomain = '<teamName>', methods=('GET', 'POST'))
def postMessage(teamName): #when someone posts a message to a team
    print("postMessage")
    #db = get_db()
    #nameQuery = db.execute('SELECT name FROM teams WHERE id = ?', (teamID,))
    #nameRows = nameQuery.fetchall()
    #name = nameRows[0]['name']
    #return returnMessages(teamID, name)

    db = get_db()
    idQuery = db.execute('SELECT id FROM teams WHERE name = ?', (teamName,))
    idRows = idQuery.fetchall()
    teamID = idRows[0]['id']
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

    return returnMessages(teamName)


