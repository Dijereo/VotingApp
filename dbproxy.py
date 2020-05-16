from datetime import datetime

from models import Election, Candidate, User, Position, db
import validate
from sendcodes import sendEmail

def authUser(username, password):
    user = User.query.get(username)
    if user and user.checkPasscode(password):
        return user

def getUser(user_id):
    return User.query.get(user_id)

def getUserId(election_id, email, passcode):
    user = User.query.filter_by(election_id=election_id, email=email).first()
    if not user:
        raise ValueError('Election or user not found', 404)
    if not user.checkPasscode(passcode):
        raise PermissionError('Invalid passcode', 401)
    return user.id

def addNewUsers(election, data, kept_emails):
    new_users = [User(election_id=election.id,
        email=user['email'], is_voter=user['is_voter'],
        has_voted=False, is_admin=user['is_admin'])
        for user in data['users'] if user['email'] not in kept_emails]
    election.users += new_users
    email_data = [(user.email, user.setPasscode()) for user in new_users]
    db.session.add(election)
    try:
        sendEmail(email_data, election.id)
    except Exception as error:
        raise error
        print(error.args)
        db.session.rollback()
        raise RuntimeError('Server not available', 503)
    db.session.commit()

def newElection(data):
    data = validate.validateElection(data)
    election = Election(name=data['election'],
        positions=[Position(title=pos['title'],
                candidates=[Candidate(name=cand['name'], votes=0)
                    for cand in pos['candidates']])
            for pos in data['positions']],
        users=[], open_time=data['open_time'],
        close_time=data['close_time'], expire_time=data['expire_time'])
    db.session.add(election)
    db.session.commit()
    addNewUsers(election, data, set())

def findElectionAndUser(election_id, user_id):
    election = Election.query.get(election_id)
    if not election:
        raise ValueError('Election not found', 404)
    user = User.query.filter_by(election_id=election_id, id=user_id).first()
    if not user:
        raise ValueError('User not found', 404)
    return election, user

def authorizeVoter(election_id, user_id):
    election, user = findElectionAndUser(election_id, user_id)
    print(datetime.now(), election.open_time, election.close_time)
    if user.has_voted:
        raise PermissionError('Voter already voted', 401)
    if datetime.now() < election.open_time:
        raise PermissionError('Election has not opened', 401)
    if datetime.now() > election.close_time:
        raise PermissionError('Election has closed', 401)
    return election, user

def getBallot(election_id, user_id):
    election, _ = authorizeVoter(election_id, user_id)
    return election.toBallot()

def castVote(election_id, user_id, ballot):
    election, user = authorizeVoter(election_id, user_id)
    new_ballot = election.toBallot()
    chosen_candidates = validate.verifyCandidates(ballot, new_ballot)
    for title, cand_name in chosen_candidates.items():
        position = Position.query.filter_by(
            election_id=election_id,
            title=title).first()
        candidate = Candidate.query.filter_by(
            position_id=position.id,
            name=cand_name).first()
        candidate.votes += 1
        db.session.add(candidate)
    user.has_voted = True
    db.session.add(user)
    db.session.commit()

def getResults(election_id, user_id):
    election, _ = findElectionAndUser(election_id, user_id)
    if election.close_time > datetime.now():
        raise PermissionError('Election still open', 401)
    if election.expire_time < datetime.now():
        raise PermissionError('Election was deleted', 410)
    return election.toResult()

def authorizeAdmin(election_id, user_id):
    election, user = findElectionAndUser(election_id, user_id)
    if not user.is_admin:
        raise PermissionError('Unauthorized', 401)
    return election, user

def getElectionData(election_id, user_id):
    election, _ = authorizeAdmin(election_id, user_id)
    return election.toData()

def getKeptEmails(election, data):
    old_emails = {user.email for user in election.users}
    return {user['email']: user for user in data['users'] if user['email'] in old_emails}

def deleteUnkeptUsers(election, kept_emails):
    kept_users = []
    while len(election.users) > 0:
        old_user = election.users[-1]
        if old_user.email in kept_emails:
            user_new_data = kept_emails[old_user.email]
            kept_users.append(User(election_id=election.id,
                email=old_user.email, passcode=old_user.passcode,
                is_voter=user_new_data['is_voter'], has_voted=False,
                is_admin=user_new_data['is_admin']))
        del election.users[-1]
    election.users = kept_users

def editElection(election, data, kept_emails):
    election.open_time = data['open_time']
    while len(election.positions) > 0:
        del election.positions[-1]
    db.session.add(election)
    db.session.commit()
    print(election.id)
    election.positions = [Position(election_id=election.id,
        title=pos['title'],
        candidates=[Candidate(name=cand['name'], votes=0)
            for cand in pos['candidates']])
        for pos in data['positions']]
    db.session.add(election)
    db.session.commit()
    deleteUnkeptUsers(election, kept_emails)
    addNewUsers(election, data, kept_emails)

def updateElection(election_id, user_id, data):
    data = validate.validateElection(data)
    election, _ = authorizeAdmin(election_id, user_id)
    election.name = data['election']
    election.close_time = data['close_time']
    election.expire_time = data['expire_time']
    kept_emails = getKeptEmails(election, data)
    if election.open_time > datetime.now():
        editElection(election, data, kept_emails)
    else:
        addNewUsers(election, data, kept_emails)

def deleteElection(election_id):
    election = Election.query.get(election_id)
    if not election:
        raise ValueError('Election not found', 404)
    if election.expire_time > datetime.now():
        raise PermissionError('Cannot delete election', 401)
    db.session.delete(election)
    db.session.commit()

def debug():
    return [el.toDict() for el in Election.query.all()]
