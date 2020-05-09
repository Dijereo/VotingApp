import json
from datetime import timedelta, datetime

from flask import Flask, request, render_template, redirect
from flask_jwt import JWT, jwt_required, current_identity
from sqlalchemy.exc import IntegrityError

from models import db, Election, User, Position, Candidate, randString
from validate import validateData, ValidationError
from sendcodes import sendEmail

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
    data = request.get_json()
    try:
        validateData(data)
    except ValidationError as error:
        return error.args
    positions = [
        Position(title=pos['title'],
            candidates=[Candidate(name=cand['name'], votes=0)
                for cand in pos['candidates']])
        for pos in data['positions']]
    users = [User(email=u['email'], is_voter=u['isVoter'],
                  has_voted=False, is_admin=u['isAdmin'])
             for u in data['users']]
    codes = [user.setPasscode() for user in users]
    sendEmail(codes)
    election = Election(name=data['election'], positions=positions, users=users,
        open_time=datetime.fromtimestamp(data['openTime'] // 1000),
        close_time=datetime.fromtimestamp(data['closeTime'] // 1000),
        expire_time=datetime.fromtimestamp(data['expireTime'] // 1000))
    db.session.add(election)
    db.session.commit()
    return 'Election created', 201

@app.route('/vote', methods=['GET'])
def goToVotePage():
    return app.send_static_file('vote.html'), 200

class AuthenticationError(Exception):
    pass

def findVoter(election_id, user_id):
    election = Election.query.get(election_id)
    if not election:
        raise AuthenticationError('Election not found', 404)
    user = Users.query.get(current_identity.id)
    if not user:
        raise AuthenticationError('Voter not found', 404)
    if user.election_id != election.id or not user.is_voter:
        raise AuthenticationError('Cannot vote in this election', 401)
    if user.has_voted:
        raise AuthenticationError('Voter already voted', 401)
    if datetime.now() < election.open_time:
        raise AuthenticationError('Election has not opened', 401)
    if datetime.now() > election.close_time:
        raise AuthenticationError('Election has closed', 401)
    return election, user

@app.route('/vote/<election_id>', methods=['GET'])
@jwt_required()
def loadBallot(election_id):
    try:
        election, user = findVoter(election_id, current_identity.id)
    except AuthenticationError as error:
        return error.args
    else:
        return json.dumps(election.toBallot()), 200

@app.route('/vote/<election_id>', methods=['PUT'])
@jwt_required()
def castVote(election_id):
    try:
        election, user = findVoter(election_id, current_identity.id)
        ballot = request.get_json()
        validateBallot(ballot)
    except (AuthenticationError, ValidationError) as error:
        return error.args
    return 'Vote Casted', 200

@app.route('/results', methods=['GET'])
def goToResultsPage():
    return app.send_static_file('results.html'), 200

@app.route('/results/<election_id>', methods=['GET'])
@jwt_required()
def getResults(election_id):
    election = Election.query.get(election_id)
    if not election:
        return 'Election not found', 404
    return json.dumps(election.toResult()), 200

@app.route('/edit', methods=['GET'])
def goToEditPage():
    return app.send_static_file('edit.html'), 200

@app.route('/edit/<election_id>', methods=['GET'])
@jwt_required()
def getElectionData(election_id):
    election = Election.query.get(election_id)
    if not election:
        return 'Election not found', 404
    return json.dumps(election.toData()), 200

@app.route('/edit/<election_id>', methods=['PUT'])
@jwt_required()
def editElection(election_id):
    election = Election.query.get(election_id)
    if not election:
        return 'Election not found', 404
    return 'Election editted', 200

@app.route('/edit/<election_id>', methods=['DELETE'])
@jwt_required()
def deleteElection(election_id):
    election = Election.query.get(election_id)
    if not election:
        return 'Election not found', 404
    return 'Deleted', 204

@app.route('/debug')
def debugDB():
    return json.dumps([el.toDict() for el in Election.query.all()]), 200

app.run(host='0.0.0.0', port=8080)


#@app.route('/signup', methods=['POST'])
#def signup():
  #userdata = request.get_json() # get userdata
  #newuser = User(username=userdata['username'], email=userdata['email']) # create user object
  #newuser.set_password(userdata['password']) # set password
  #try:
    #db.session.add(newuser)
    #db.session.commit() # save user
  #except IntegrityError: # attempted to insert a duplicate user
    #db.session.rollback()
    #return 'username or email already exists' # error message
  #return 'user created'