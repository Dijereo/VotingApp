import re
import time
from datetime import timedelta, datetime
from models import Election, User, Position, Candidate, db
from sendcodes import sendEmail

email_regex = re.compile(r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)')

def validateEmail(email):
    if email_regex.fullmatch(email) is None:
        raise ValueError()

def validateTimes(open_time, close_time, expire_time):
    open_time = datetime.fromtimestamp(open_time // 1000)
    close_time = datetime.fromtimestamp(close_time // 1000)
    expire_time = datetime.fromtimestamp(expire_time // 1000)
    now = datetime.now()
    if open_time < now:
        open_time = now
    elif open_time - now > timedelta(days=100):
        open_time = now + timedelta(days=100)
    if close_time - open_time < timedelta(minutes=5):
        close_time = open_time + timedelta(minutes=5)
    elif close_time - open_time > timedelta(days=50):
        close_time = open_time + timedelta(days=50)
    if expire_time - close_time < timedelta(hours=1):
        expire_time = close_time + timedelta(hours=1)
    elif expire_time - close_time > timedelta(days=366):
        expire_time  = close_time + timedelta(days=366)
    return open_time, close_time, expire_time

def validateElection(data):
    try:
        data['election'] = str(data.get('election', ''))
        data['positions'] = list(data.get('positions', []))
        for pos in data['positions']:
            pos['title'] = str(pos.get('title', ''))
            pos['candidates'] = list(pos.get('candidates', []))
            for cand in pos['candidates']:
                cand['name'] = str(cand.get('name', ''))
        emails = set()
        data['users'] = list(data.get('users', []))
        users = []
        for u in data['users']:
            email = str(u.get('email', ''))
            validateEmail(email)
            if email in emails:
                continue
            emails.add(email)
            user = {'email': email}
            user['is_voter'] = bool(u.get('isVoter', False))
            user['is_admin'] = bool(u.get('isAdmin', False))
            users.append(user)
        data['users'] = users
        data['open_time'], data['close_time'], data['expire_time'] = validateTimes(
            int(data.get('openTime', 0)),
            int(data.get('closeTime', 0)),
            int(data.get('expireTime', 0)))
    except Exception as err:
        print(err.args)
        return None
    else:
        return data

def updateElection(data, election):
    data = validateElection(data)
    if data is None:
        return
    election.name = data['election']
    if election.open_time > datetime.now():
        while len(election.positions) > 0:
            del election.positions[-1]
        election.positions = [
            Position(
                title=pos['title'],
                candidates=[
                    Candidate(name=cand['name'], votes=0)
                    for cand in pos['candidates']])
            for pos in data['positions']]
        election.open_time = data['open_time']
        election.close_time = data['close_time']
        election.expire_time = data['expire_time']
        new_emails = set(u['email'] for u in data['users'])
        kept_users = []
        while len(election.users) > 1:
            user = election.users[-1]
            if user.email in new_emails:
                kept_users.append(
                    User(email=user.email,
                        passcode=user.passcode,
                        is_voter=user.is_voter,
                        has_voted=False,
                        is_admin=user.is_admin))
            del election.users[-1]
        election.users = kept_users
    else:
        if data['close_time'] > election.close_time:
            election.close_time = data['close_time']
        if data['expire_time'] > election.expire_time:
            election.expire_time = data['expire_time']
    old_emails = set(user.email for user in election.users)
    codes = []
    new_users = []
    for user in data['users']:
        if user['email'] not in old_emails:
            new_users.append(
                User(email=user['email'],
                    is_voter=user['is_voter'],
                    has_voted=False,
                    is_admin=user['is_admin']))
            codes.append(new_users[-1].setPasscode())
    election.users += new_users
    db.session.add(election)
    db.session.commit()
    sendEmail(codes)

def validateBallot(ballot):
    pass