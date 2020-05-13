function newCandidate() {
  return {name: ''};
}

function newPosition() {
  return {title: '', candidates: []};
}

function newUser() {
  return {email: '', isVoter: true, isAdmin: false};
}

function readPositionData(posDOM) {
  let position = newPosition();
  position.title = posDOM.getElementsByClassName('title-input')[0].value;
  let candDOMs = posDOM.getElementsByClassName('cand-input');
  for (let candDOM of candDOMs) {
    let candidate = newCandidate();
    candidate.name = candDOM.value;
    position.candidates.push(candidate);
  }
  return position;
}

function readUserData(userDOM) {
  let user = newUser();
  user.email = userDOM.getElementsByClassName('email-input')[0].value;
  user.isVoter = userDOM.getElementsByClassName('voter-input')[0].checked;
  user.isAdmin = userDOM.getElementsByClassName('admin-input')[0].checked;
  return user;
}

function readDatetime(form, field) {
  return (new Date(
    form[field].value.slice(0, 16)
  )).getTime()
}

function readElectionForm(formId) {
  let form = document.forms[formId];
  let electionData = {
    election: form['election'].value,
    positions: [],
    users: [],
    openTime: readDatetime(form, 'open-time'),
    closeTime: readDatetime(form, 'close-time'),
    expireTime: readDatetime(form, 'expire-time')
  };
  for (let posDiv of document.getElementsByClassName('pos-div')) {
    electionData.positions.push(readPositionData(posDiv));
  }
  for (let userDiv of document.getElementsByClassName('user-div')) {
    electionData.users.push(readUserData(userDiv));
  }
  return electionData;
}
