import json
from datetime import timedelta, datetime

from flask import Flask, request, render_template, redirect
from flask_jwt import JWT, jwt_required, current_identity
from sqlalchemy.exc import IntegrityError

from models import db, Election, User, Position, Candidate, randString
import validate
from sendcodes import sendEmail
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
    user = User.query.get(username)
    if user and user.checkPasscode(password):
        return user

def identity(payload):
    return User.query.get(payload['identity'])

jwt = JWT(app, authenticate, identity)

@app.route('/', methods=['GET'])
def index():
	  return app.send_static_file('index.html'), 200

@app.route('/', methods=['POST'])
def getUserId():
    user_data = request.get_json()
    election_id = user_data['electionId']
    passcode = user_data['passcode']
    email = user_data['email']
    user = User.query.filter_by(election_id=election_id, email=email).first()
    if not user:
        return 'Election or user not found', 404
    if not user.checkPasscode(passcode):
        return 'Invalid passcode', 401
    return json.dumps({'user_id': user.id}), 200

@app.route('/create', methods=['GET'])
def goToCreatePage():
    return app.send_static_file('create.html'), 200

@app.route('/create', methods=['POST'])
def createElection():
    data = validateElection(request.get_json())
    if data is None:
        return 'Invalid Data', 400
    success = proxy.newElection(data)
    if not success:
        return 'Server Error - Try Again', 500
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
        return error.args
    else:
        return json.dumps(ballot), 200

@app.route('/vote/<election_id>', methods=['PUT'])
@jwt_required()
def castVote(election_id):
    ballot = request.get_json()
    ballot = validate.validateBallot(ballot)
    if ballot is None:
        return 'Invalid Data', 400
    try:
        dbproxy.castVote(election_id, current_identity.id, ballot)
    except Exception as error:
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
        return error.args
    return json.dumps(election), 200

@app.route('/edit/<election_id>', methods=['PUT'])
@jwt_required()
def editElection(election_id):
    data = request.get_json()
    success = dbproxy.updateElection(election_id, user_id, data)
    if not success:
        return 'Server Error - Try Again', 500
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
    return json.dumps([el.toDict() for el in Election.query.all()]), 200

app.run(host='0.0.0.0', port=8080)
