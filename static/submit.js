// Requires auth.js

let host = 'https://votingtest--dijereo.repl.co';

function submit(event) {
  event.preventDefault();
}

function redirect(path) {
  window.location.href = `${host}${path}`;
}

async function postJSONData(path, body, includeToken) {
  let data = {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(body)
  }
  if (includeToken) {
    data.headers['Authorization'] = `JWT ${loadToken()}`;
  }
  let response = await fetch(`${host}${path}`, data);
  return response;
}

async function putJSONData(path, body, includeToken) {
  let data = {
    method: 'PUT',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(body)
  }
  if (includeToken) {
    data.headers['Authorization'] = `JWT ${loadToken()}`;
  }
  let response = await fetch(`${host}${path}`, data);
  return response;
}
