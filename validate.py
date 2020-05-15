from datetime import timedelta, datetime

def validateCandidates(candidates):
    unique_candidates = {}
    for cand in candidates:
        cand['name'] = str(cand.get('name', ''))
        unique_candidates[cand['name']] = cand
    return list(unique_candidates.values())

def validatePositions(positions):
    unique_positions = {}
    for pos in positions:
        pos['title'] = str(pos.get('title', ''))
        unique_positions[pos['title']] = pos
        pos['candidates'] = validateCandidates(list(pos.get('candidates', [])))
    return list(unique_positions.values())

def validateUsers(users):
    unique_users = {}
    for user in users:
        user['email'] = str(user.get('email', ''))
        unique_users[user['email']] = user
        user['is_voter'] = bool(user.get('isVoter', False))
        user['is_admin'] = bool(user.get('isAdmin', False))
    return list(unique_users.values())

def validateTime(js_timestamp, earliest, latest):
    dt = datetime.fromtimestamp(js_timestamp // 1000)
    return max(earliest, min(latest, dt))

def validateTimes(js_open_time, js_close_time, js_expire_time):
    now = datetime.now()
    open_time = validateTime(js_open_time, now, now + timedelta(days=120))
    close_time = validateTime(js_close_time,
        open_time + timedelta(minutes=5),
        open_time + timedelta(days=120))
    expire_time = validateTime(js_expire_time,
        close_time + timedelta(minutes=5),
        close_time + timedelta(days=120))
    return open_time, close_time, expire_time

def validateElection(data):
    try:
        data['election'] = str(data.get('election', ''))
        data['positions'] = validatePositions(list(data.get('positions', [])))
        data['users'] = validateUsers(list(data.get('users', [])))
        data['open_time'], data['close_time'], data['expire_time'] = validateTimes(
            int(data.get('openTime', 0)),
            int(data.get('closeTime', 0)),
            int(data.get('expireTime', 0)))
    except Exception as error:
        print(error.args)
        raise ValueError('Invalid Data', 500)
    return data

def validateBallot(ballot):
    try:
        unique_positions = {}
        ballot['positions'] = list(ballot.get('positions', []))
        for pos in ballot['positions']:
            pos['title'] = str(pos.get('title'), '')
            pos['candidate'] = str(pos.get('candidate'))
            unique_positions[pos['title']] = pos
        ballot['positions'] = list(unique_positions.values())
    except Exception as error:
        print(error.args)
        raise ValueError('Invalid Data', 500)
    return ballot

def verifyCandidates(ballot, new_ballot):
    chosen_candidates = {}
    titles = [pos['title'] for pos in new_ballot['positions']]
    print(titles)
    for pos in ballot['positions']:
        try:
            print(pos['title'])
            i = titles.index(pos['title'])
            print(i)
        except ValueError:
            continue
        cands = [cand['name'] for cand in new_ballot['positions'][i]['candidates']]
        print(cands)
        try:
            print(pos['candidate'])
            j = cands.index(pos['candidate'])
            print(j)
        except ValueError:
            continue
        chosen_candidates[titles[i]] = cands[j]
        print(chosen_candidates)
    print(chosen_candidates)
    return chosen_candidates
