from datetime import timedelta
import json

from flask import Flask, request, render_template, redirect
from flask_jwt import JWT, jwt_required, current_identity
from sqlalchemy.exc import IntegrityError

from models import db, randString
import dbproxy

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    app.config['SECRET_KEY'] = randString(8)
    app.config['JWT_EXPIRATION_DELTA'] = timedelta(days=7)
    db.init_app(app)
    return app

app = create_app()
app.app_context().push()
db.create_all(app=app)

def authenticate(username, password):
    return dbproxy.authUser(username, password)

def identity(payload):
    return dbproxy.getUser(payload['identity'])

jwt = JWT(app, authenticate, identity)

@app.route('/', methods=['GET'])
def index():
	  return app.send_static_file('index.html'), 200

@app.route('/', methods=['POST'])
def getUserId():
    user_data = request.get_json()
    try:
        user_id = dbproxy.getUserId(user_data['electionId'],
            user_data['email'], user_data['passcode'])
    except Exception as error:
        return error.args
    return json.dumps({'user_id': user_id}), 200

@app.route('/create', methods=['GET'])
def goToCreatePage():
    return app.send_static_file('create.html'), 200

@app.route('/create', methods=['POST'])
def createElection():
    data = request.get_json()
    try:
        dbproxy.newElection(data)
    except Exception as error:
        return error.args
    return 'Election created', 201

@app.route('/vote', methods=['GET'])
def goToVotePage():
    return app.send_static_file('vote.html'), 200

@app.route('/vote/<election_id>', methods=['GET'])
@jwt_required()
def loadBallot(election_id):
    try:
        ballot = dbproxy.getBallot(election_id, current_identity.id)
    except Exception as error:
        print(error.args)
        return error.args
    else:
        return json.dumps(ballot), 200

@app.route('/vote/<election_id>', methods=['PUT'])
@jwt_required()
def castVote(election_id):
    ballot = request.get_json()
    try:
        dbproxy.castVote(election_id, current_identity.id, ballot)
    except Exception as error:
        print(error.args)
        return error.args
    return 'Vote Casted', 200

@app.route('/results', methods=['GET'])
def goToResultsPage():
    return app.send_static_file('results.html'), 200

@app.route('/results/<election_id>', methods=['GET'])
@jwt_required()
def getResults(election_id):
    try:
        results = dbproxy.getResults(election_id, current_identity.id)
    except Exception as error:
        print(error.args)
        return error.args
    return json.dumps(results), 200

@app.route('/edit', methods=['GET'])
def goToEditPage():
    return app.send_static_file('edit.html'), 200

@app.route('/edit/<election_id>', methods=['GET'])
@jwt_required()
def getElectionData(election_id):
    try:
        election = dbproxy.getElectionData(election_id, current_identity.id)
    except Exception as error:
        print(error.args)
        return error.args
    return json.dumps(election), 200

@app.route('/edit/<election_id>', methods=['PUT'])
@jwt_required()
def editElection(election_id):
    data = request.get_json()
    try:
        dbproxy.updateElection(election_id, current_identity.id, data)
    except Exception as error:
        return error.args
    return 'Election updated', 200

@app.route('/remove/<election_id>', methods=['DELETE'])
def deleteElection(election_id):
    try:
        dbproxy.deleteElection(election_id)
    except Exception as error:
        return error.args
    return 'Deleted', 204

@app.route('/debug')
def debugDB():
    return json.dumps(dbproxy.debug()), 200

app.run(host='0.0.0.0', port=8080)
