function removeButtonHTML(onclick) {
  return `<button class="remove-button" type="button" onclick="${onclick}">-</button>`;
}

function removeOnClick(button) {
  button.parentNode.parentNode.removeChild(button.parentNode);
}

function addButtonHTML(onclick) {
  return `<button class="add-button" type="button" onclick="${onclick}">+</button>`;
}

function candidateHTML(candidate) {
  return `
    <div class="cand-div">
      ${removeButtonHTML("removeOnClick(this)")}
      <input type="text" class="cand-input" value="${candidate.name}">
    </div>
  `
}

function addCandidate(candListDiv) {
  candListDiv.innerHTML += candidateHTML(newCandidate())
}

function positionHTML(positionData) {
  let html = `
    <div class="pos-div">
      ${removeButtonHTML("removeOnClick(this)")}
      <div class="title-div">
        <label class="title-label">Position Title</label>
        <input class="title-input" value="${positionData.title}">
      </div>
      <div class="cand-list-div">
        <label class="cand-label">Candidates</label>
        ${addButtonHTML("addCandidate(this.parentNode)")}`;
  for (let candidate of positionData.candidates) {
    html += candidateHTML(candidate);
  }
  html += `</div></div>`;
  return html;
}

function addPosition() {
  let positionsDiv = document.querySelector('#positions');
  positionsDiv.innerHTML += positionHTML(newPosition());
}

function userHTML(user) {
  return `
    <div class="user-div">
      ${removeButtonHTML("removeOnClick(this)")}
      <div class="email-div">
        <label class="email-label">Email</label>
        <input class="email-input" type="email" value="${user.email}">
      </div>
      <div class="voter-div">
        <label class="voter-label">Voter</label>
        <input class="voter-input" type="checkbox" ${user.isVoter ? "checked" : ""}>
      </div>
      <div class="admin-div">
        <label class="admin-label">Admin</label>
        <input class="admin-input" type="checkbox" ${user.isAdmin ? "checked" : ""}>
      </div>
    </div>
  `;
}

function addUser() {
  let userDiv = document.querySelector('#users');
  userDiv.innerHTML += userHTML(newUser());
}

function getLocalISODate(timestamp) {
  let date = new Date(timestamp);
  let tz = date.getTimezoneOffset();
  let local = date - tz * 60 * 1000;
  return (new Date(local)).toISOString().slice(0, 16);
}

function renderElectionData(electionData, formId) {
  let form = document.forms[formId];
  console.log(electionData);
  form['election'].value = electionData.election;
  let positionDiv = document.querySelector('#positions');
  positionDiv.innerHTML += addButtonHTML("addPosition()");
  for (let position of electionData.positions) {
    positionDiv.innerHTML += positionHTML(position);
  }
  let userDiv = document.querySelector('#users');
  userDiv.innerHTML += addButtonHTML("addUser()");
  for (let user of electionData.users) {
    userDiv.innerHTML += userHTML(user);
  }
  form['open-time'].value = getLocalISODate(electionData.openTime);
  form['close-time'].value = getLocalISODate(electionData.closeTime);
  form['expire-time'].value = getLocalISODate(electionData.expireTime);
}