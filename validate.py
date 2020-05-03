import re
import time
from datetime import timedelta, datetime

class ValidationError(Exception):
    pass

email_regex = re.compile(r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)')

def validateEmail(email):
    if email_regex.fullmatch(email) is None:
        raise ValidationError(f'Invalid email address', 400)

def validateTimes(open_time, close_time, expire_time):
    open_time = datetime.fromtimestamp(open_time // 1000)
    close_time = datetime.fromtimestamp(close_time // 1000)
    expire_time = datetime.fromtimestamp(expire_time // 1000)
    now = datetime.now()
    if open_time < now:
        raise ValidationError('Opening time must be in future', 400)
    if open_time - now > timedelta(days=100):
        raise ValidationError('Opening time cannot be more than 100 days away', 400)
    if close_time - open_time < timedelta(minutes=5):
        raise ValidationError('Election must be open for at least 5 minutes', 400)
    if close_time - open_time > timedelta(days=50):
        raise ValidationError('Election cannot be open for more than 50 days', 400)
    if expire_time - close_time < timedelta(hours=1):
        raise ValidationError('Election must be available for at least an hour', 400)
    if expire_time - close_time > timedelta(days=366):
        raise ValidationError('Election cannot be available for more than a year', 400)

def validateAttribute(object_, attribute, expected_type):
    try:
        value = object_[attribute]
    except KeyError:
        raise ValidationError(f'"{attribute}" missing', 400)
    if type(value) is not expected_type:
        raise ValidationError(f'"{attribute}" must be type "{expected_type.__name__}"', 400)
    if expected_type in (str, list) and len(value) == 0:
        raise ValidationError(f'"{attribute}" must not be empty', 400)

def validateData(data):
    validateAttribute(data, 'election', str)
    validateAttribute(data, 'positions', list)
    for pos in data['positions']:
        validateAttribute(pos, 'title', str)
        validateAttribute(pos, 'candidates', list)
        for cand in pos['candidates']:
            validateAttribute(cand, 'name', str)
    validateAttribute(data, 'users', list)
    for user in data['users']:
        validateAttribute(user, 'email', str)
        validateEmail(user['email'])
        validateAttribute(user, 'isVoter', bool)
        validateAttribute(user, 'isAdmin', bool)
    validateAttribute(data, 'openTime', int)
    validateAttribute(data, 'closeTime', int)
    validateAttribute(data, 'expireTime', int)
    validateTimes(data['openTime'], data['closeTime'], data['expireTime'])
