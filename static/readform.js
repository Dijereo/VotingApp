let emptyData = {
  election: '', positions: [], users: [],
  openTime: Date.now(), closeTime: Date.now(), expireTime: Date.now()
};

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

function convertElectionData(electionData) {
  for (let user of electionData.users) {
      user.isVoter = user.is_voter;
      user.isAdmin = user.is_admin;
    }
  electionData.openTime = electionData.open_time * 1000;
  electionData.closeTime = electionData.close_time * 1000;
  electionData.expireTime = electionData.expire_time * 1000;
}

async function getElectionData() {
  let electionId = sessionStorage.getItem(electionIdLookup);
  let response = await sendRequest(
    `/edit/${electionId}`, 'GET', null, true
  );
  if (response.ok) {
    let electionData = await response.json();
    electionData = convertElectionData(electionData);
  }
}

async function editElection(formId, electionData) {
  let electionId = sessionStorage.getItem(electionIdLookup);
  let response = await sendRequest(
    `/edit/${electionId}`, 'PUT', electionData, true
  );
  if (response.ok) {
    alert('Election Editted');
    redirect('/');
  } else {
    alert('Error occurred - Check data entered');
  }
}
