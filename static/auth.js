let tokenLookup = 'user-token';
let electionIdLookup = 'election-id';

async function obtainUserId(electionId, email, passcode) {
  let body = {
    'electionId': electionId, 'email': email, 'passcode': passcode
  };
  let response = await sendRequest('/', 'POST', body, false);
  if (response.ok) {
    let result = await response.json();
    return result.user_id;
  } else {
    return 0;
  }
}

async function obtainToken(userId, passcode) {
  let body = {
    'username': userId, 'password': passcode
  };
  let response = await sendRequest('/auth', 'POST', body, false);
  if (response.ok) {
    let result = await response.json();
    return result.access_token;
  } else {
    return '';
  }
}

async function authenticate(path, formId) {
  let form = document.forms[formId];
  let electionId = form['election-id'].value;
  let passcode = form['passcode'].value;
  let email = form['email'].value;
  let userId = await obtainUserId(electionId, email, passcode);
  if (userId === 0) {
    alert('User not found');
    return;
  }
  let token = await obtainToken(userId, passcode);
  if (token) {
    sessionStorage.setItem(tokenLookup, token);
    sessionStorage.setItem(electionIdLookup, electionId);
    redirect(path);
  } else {
    alert('Incorrect passcode');
  }
}
