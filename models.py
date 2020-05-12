from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import string
import secrets

db = SQLAlchemy()

def randString(length):
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))

class Election(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    positions = db.relationship('Position', backref='election')
    users = db.relationship('User', backref='election')
    open_time = db.Column(db.DateTime, nullable=False)
    close_time = db.Column(db.DateTime, nullable=False)
    expire_time = db.Column(db.DateTime, nullable=False)

    def toData(self):
        return {'election': self.name,
                'positions': [pos.toData() for pos in self.positions],
                'users': [user.toData() for user in self.users],
                'open_time': int(self.open_time.timestamp()),
                'close_time': int(self.close_time.timestamp()),
                'expire_time': int(self.expire_time.timestamp())}

    def toResult(self):
        return {'election': self.name,
                'positions': [pos.toResult() for pos in self.positions],
                'expire_time': int(self.expire_time.timestamp())}

    def toBallot(self):
        return {'election': self.name,
                'positions': [pos.toBallot() for pos in self.positions],
                'close_time': int(self.close_time.timestamp())}

    def toDict(self):
        return {'id': self.id, 'election': self.name,
                'positions': [pos.toDict() for pos in self.positions],
                'users': [user.toDict() for user in self.users],
                'open_time': int(self.open_time.timestamp()),
                'close_time': int(self.close_time.timestamp()),
                'expire_time': int(self.expire_time.timestamp())}

class Position(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    election_id = db.Column(db.Integer, db.ForeignKey('election.id'), nullable=False)
    title = db.Column(db.String(80), nullable=False)
    candidates = db.relationship('Candidate', backref='position')

    def toData(self):
        return {'id': self.id,
                'title': self.title,
                'candidates': [cand.toData() for cand in self.candidates]}
    
    def toResult(self):
        return {'title': self.title,
                'candidates': [cand.toResult() for cand in self.candidates]}

    def toBallot(self):
        return {'title': self.title,
                'candidates': [cand.toBallot() for cand in self.candidates]}

    def toDict(self):
        return {'id': self.id, 'election_id': self.election_id, 'title': self.title,
                'candidates': [cand.toDict() for cand in self.candidates]}

class Candidate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    position_id = db.Column(db.Integer, db.ForeignKey('position.id'), nullable=False)
    name = db.Column(db.String(80), nullable=False)
    votes = db.Column(db.Integer, nullable=False)

    def toData(self):
        return {'id': self.id, 'name': self.name}

    def toResult(self):
        return {'name': self.name, 'votes': self.votes}

    def toBallot(self):
        return {'name': self.name}

    def toDict(self):
        return {'id': self.id, 'position_id': self.position_id, 'name': self.name,
                'votes': self.votes}

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    election_id = db.Column(db.Integer, db.ForeignKey('election.id'), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    passcode = db.Column(db.String(12), nullable=False)
    is_voter = db.Column(db.Boolean, nullable=False)
    has_voted = db.Column(db.Boolean, nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False)

    def setPasscode(self):
        passcode = randString(16)
        self.passcode = generate_password_hash(passcode, method='sha256')
        return self.email, passcode
    
    def checkPasscode(self, passcode):
        return check_password_hash(self.passcode, passcode)

    def toData(self):
        return {'id': self.id, 'email': self.email, 'is_voter': self.is_voter,
                'is_admin': self.is_admin}

    def toDict(self):
        return {'id': self.id, 'election_id': self.election_id, 'email': self.email,
                'passcode': self.passcode, 'is_voter': self.is_voter,
                'has_voted': self.has_voted, 'is_admin': self.is_admin}
