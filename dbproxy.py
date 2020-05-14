from datetime import datetime

from models import Election, Candidate, User, Position

def newElection(data):
    election = Election(name=data['election'],
        positions=[Position(title=pos['title'],
                candidates=[Candidate(name=cand['name'], votes=0)
                    for cand in pos['candidates']])
            for pos in data['positions']],
        users=[User(email=user['email'], is_voter=user['is_voter'],
            has_voted=False, is_admin=user['is_admin'])
            for user in data['users']],
        open_time=data['open_time'],
        close_time=data['close_time'],
        expire_time=data['expire_time'])
    email_data = [(user.email, user.setPasscode()) for user in election.users]
    db.session.add(election)
    try:
        sendEmail(codes, election.id)
        db.session.commit()
        return True
    except:
        db.session.rollback()
        return False

def getBallot(election_id, user_id):
    election = Election.query.get(election_id)
    if not election:
        raise ValueError('Election not found', 404)
    user = Users.query.filter_by(
        election_id=election_id,
        id=user_id).first()
    if not user:
        raise ValueError('Voter not found', 404)
    if user.has_voted:
        raise PermissionError('Voter already voted', 401)
    if datetime.now() < election.open_time:
        raise PermissionError('Election has not opened', 401)
    if datetime.now() > election.close_time:
        raise PermissionError('Election has closed', 401)
    return election.toBallot()

def castVote(election_id, user_id, ballot):
    new_ballot = getBallot(election_id, user_id)
    chosen_candidates = verifyCandidates(ballot, new_ballot)
    titles = [pos['title'] for pos in new_ballot['positions']]
    for title, cand_name in chosen_candidates.items():
        position = Position.query.filter_by(
            election_id=election_id,
            title=title).first()
        candidate = candidate.query.filter_by(
            position_id=position.id,
            name=cand_name).first()
        candidate.votes += 1
        db.session.add(candidate)
    db.session.commit()

def getResults(election_id, user_id)
    election = Election.query.get(election_id)
    if not election:
        raise ValueError('Election not found', 404)
    user = User.query.filter_by(
        election_id=election_id,
        id=user_id).first()
    if not user:
        raise ValueError('User not found', 404)
    if election.close_time > datetime.now():
        raise ValueError('Election still open', 401)
    return election.toResults()

def getElectionData(election_id, user_id):
    election = Election.query.get(election_id)
    if not election:
        raise ValueError('Election not found', 404)
    user = User.query.filter_by(
        election_id=election_id,
        id=current_identity.id).first()
    if not user:
        raise ValueError('User not found', 404)
    if not user.is_admin:
        raise PermissionError('Unauthorized', 401)
    return election.toData()

def authorizeAdmin(election_id, user_id):
    election = Election.query.get(election_id)
    if not election:
        raise ValueError('Election not found', 404)
    user = User.query.filter_by(election_id=election_id, id=user_id).first()
    if not user:
        raise ValueError('User not found', 404)
    if not user.is_admin:
        raise PermissionError('Unauthorized', 401)
    return election, user

def getKeptEmails(election, data):
    old_emails = {user.email for user in election.users}
    return {user['email']: user for user in data['users'] if user['email'] in old_emails}

def addNewUsers(election, data, kept_emails):
    new_users = [User(email=user['email'], is_voter=user['is_voter'],
        has_voted=False, is_admin=user['is_admin'])
        for user in data['users'] if user['email'] not in kept_emails]
    election.users += added_users
    email_data = [(user.email, user.setPasscode()) for user in added_users]
    db.session.add(election)
    try:
        sendEmail(email_data, election.id)
        db.session.commit()
        return True
    except:
        db.session.rollback()
        return False

def deleteUnkeptUsers(election, kept_emails):
    kept_users = []
    while len(election.users) > 0:
        old_user = election.users[-1]
        if old_user.email in kept_emails:
            user_new_data = kept_emails[old_user.email]
            kept_users.append(User(email=old_user.email, passcode=old_user.passcode,
                is_voter=user_new_data['is_voter'], has_voted=False,
                is_admin=user_new_data['is_admin']))
        del election.users[-1]
    election.users = kept_users

def editElection(election, data, kept_emails):
    election.open_time = data['open_time']
    while len(election.positions > 0):
        del election.positions[-1]
    election.positions = [Position(title=pos['title'],
        candidates=[Candidate(name=cand['name'], votes=0)
            for cand in pos['candidates']])
        for pos in data['positions']]
    deleteUnkeptUsers(election, kept_emails)
    return addNewUsers(election, data, kept_emails):

def updateElection(election_id, user_id, data):
    data = validateElection(data)
    election, _ = authorizeAdmin(election_id, user_id)
    election.name = data['election']
    election.close_time = data['close_time']
    election.expire_time = data['expire_time']
    kept_emails = getKeptEmails(election, data)
    if election.open_time > datetime.now():
        return editElection(election, data, kept_emails)
    return addNewUsers(election, data, kept_emails)

def deleteElection(election_id):
    election = Election.query.get(election_id)
    if not election:
        raise ValueError('Election not found', 404)
    if election.expire_time > datetime.now():
        raise PermissionError('Cannot delete election', 401)
    db.session.delete(election)
    db.session.commit()
