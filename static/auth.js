// Requires submit.js

let tokenLookup = 'user-token';
let electionIdLookup = 'election-id';

function loadToken() {
  let token = sessionStorage.getItem(tokenLookup);
  return token;
}

function loadElectionId() {
  let electionId = sessionStorage.getItem(electionIdLookup);
  return electionId;
}

function setTokenAndId(token, electionId) {
  sessionStorage.setItem(tokenLookup, token);
  sessionStorage.setItem(electionIdLookup, electionId);
}

async function obtainUserId(electionId, email, passcode) {
  let body = {
    'electionId': electionId, 'email': email, 'passcode': passcode
  };
  let response = await postJSONData('/', body, false);
  if (response.ok) {
    let result = await response.json();
    return result.user_id;
  }
  return 0;
}

async function obtainToken(userId, passcode) {
  let body = {
    'username': userId, 'password': passcode
  };
  let response = await postJSONData('/auth', body, false);
  if (response.ok) {
    let result = await response.json();
    return result.access_token;
  }
  return '';
}

async function authenticate(path, formId) {
  let form = document.forms[formId];
  // TODO: Form validation
  let electionId = form['election-id'].value;
  let passcode = form['passcode'].value;
  let email = form['email'].value;
  let userId = await obtainUserId(electionId, email, passcode);
  console.log(userId);
  if (userId === 0) {
    alert('Invalid Data 1');
    return;
  }
  let token = await obtainToken(userId, passcode);
  if (token) {
    setTokenAndId(token, electionId);
    redirect(path);
  } else {
    alert('Invalid Data 2');
  }
}
