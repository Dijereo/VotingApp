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

function storeElectionData(formId) {
  let form = document.forms[formId];
  let electionData = {
    election: form['election'].value, positions: [], users: [],
    openTime: (new Date(form['open-time'].value.slice(0, 16))).getTime(),
    closeTime: (new Date(form['close-time'].value.slice(0, 16))).getTime(),
    expireTime: (new Date(form['expire-time'].value.slice(0, 16))).getTime()
  };
  let positionsDivs = document.getElementsByClassName('pos-div');
  for (let posDiv of positionsDivs) {
    electionData.positions.push(readPositionData(posDiv));
  }
  let userDivs = document.getElementsByClassName('user-div');
  for (let userDiv of userDivs) {
    electionData.users.push(readUserData(userDiv));
  }
  return electionData;
}

async function postElection(formId) {
  let electionData = storeElectionData(formId);
  let response = await postJSONData('/create', electionData, false);
  if (response.ok) {
    redirect('/');
  }
}

async function getResults() {
  let token = loadToken();
  let electionId = loadElectionId();
  let response = await fetch(
    `${host}/results/${electionId}`,
    {
      headers: {'Authorization': `JWT ${token}`}
    }
  );
  let result = await response.json();
  return response.ok ? result : null;
}

async function loadResults() {
  results = await getResults();
  if (results === null) {
    redirect('/');
  }
  document.querySelector('#name').innerHTML = results.election;
  let resultsDiv = document.querySelector('#results');
  resultsDiv.innerHTML = "";
  for (let position of results.positions) {
    resultsDiv.innerHTML += `<h3>${position.title}</h3><table>`;
    for (let candidate of position.candidates) {
      resultsDiv.innerHTML += `<tr><td>${candidate.name}</td><td>${canidate.votes}</td></tr>`;
    }
    resultsDiv.innerHTML`</table>`;
  }
}

async function getBallot() {
  let token = loadToken();
  let electionId = loadElectionId();
  let response = await fetch(
    `${host}/vote/${electionId}`,
    {
      headers: {'Authorization': `JWT ${token}`}
    }
  );
  let result = await response.json();
  return response.ok ? result : null;
}

async function loadBallot() {
  results = await getBallot();
  if (results === null) {
    // This user is not allowed to vote or they were logged out
    // Add code to notfify them
    redirect('/');
  }
  // Insert code to dipslay the ballot on screen
  // use results.election to get the election's name
  for (let position of results.positions) {
    // loop through each position
    // use position.title to get the positions name
    for (let candidate of position.candidates) {
      // loop through each candidate of the position
      // use candidate.name to get the candidate's name
    }
  }
}

async function getElectionData() {
  let token = loadToken();
  let electionId = loadElectionId();
  let response = await fetch(
    `${host}/edit/${electionId}`,
    {
      headers: {'Authorization': `JWT ${token}`}
    }
  );
  if (response.ok) {
    let result = await response.json();
    console.log(result);
    for (let user of result.users) {
      user.isVoter = user.is_voter;
      user.isAdmin = user.is_admin;
    }
    result.openTime = result.open_time * 1000;
    result.closeTime = result.close_time * 1000;
    result.expireTime = result.expire_time * 1000;
    renderElectionData(result, 'edit-form');
  }
}

async function editElection(formId) {
  let electionId = loadElectionId()
  let electionData = storeElectionData(formId);
  let response = await putJSONData(`/edit/${electionId}`, electionData, true);
  if (response.ok) {
    redirect('/');
  }
}
