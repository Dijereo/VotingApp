let MOCK = false;

let host = 'https://votingtest--dijereo.repl.co';

function submit(event) {
  event.preventDefault();
}

function redirect(path) {
  window.location.href = `${host}${path}`;
}

async function sendRequest(path, method, body, includeToken) {
  let data = {
    method: method,
    headers: {}
  }
  if (body !== null) {
    data.headers['Content-Type'] = 'application/json';
    data.body = JSON.stringify(body);
  }
  if (includeToken) {
    let token = sessionStorage.getItem(tokenLookup);
    data.headers['Authorization'] = `JWT ${token}`;
  }
  let response = await fetch(`${host}${path}`, data);
  return response;
}
