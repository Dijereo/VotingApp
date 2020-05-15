let mockBallot = {
  'election': 'Mock Election',
  'positions': [
    { 'title': 'President',
      'candidates': [
        {'name': 'John Doe'},
        {'name': 'Mary Sue'}
      ]
    },
    { 'title': 'Vice President',
      'candidates': [
        {'name': 'Joe Bob'},
        {'name': 'No Confidence'}
      ]
    }
  ]
};

async function getBallot() {
  let electionId = sessionStorage.getItem(electionIdLookup);
  let response = await sendRequest(`/vote/${electionId}`, 'GET', null, true);
  if (response.ok) {
    let result = await response.json();
    return result;
  }
  return null;
}

function loadBallot(electionData) {
  if (electionData === null) {
    alert("Cannot access election");
    redirect("/");
  }
  document.querySelector("#election").innerHTML = electionData.election;
  let ballotDiv = document.querySelector("#ballot");
  let html = "";
  html = `<form id="vote-form">`;
  for (let position of electionData.positions) {
    html += `<h2 id="pos-title">${position.title}</h2>`;
    for (let candidate of position.candidates) {
      html += `
        <label id="form-label" for="${candidate.name}">
          <input type="radio" name="${position.title}" id="${candidate.name}"
            value="${candidate.name}"/>${candidate.name}</label>`;
    }
  }
  html += `
    </br>
    <button class="vote-form-button" type="button"
      onclick="castVote(getBallotData('vote-form'))">Vote</button>`;
  html += `</form>`;
  ballotDiv.innerHTML = html;
  document.forms['vote-form'].addEventListener('submit', submit);
}

function getBallotData(formId) {
  let form = document.forms[formId];
  // TODO
}

async function castVote(ballot) {
  let electionId = sessionStorage.getItem(electionIdLookup);
  let response = await sendRequest(`/vote/${electionId}`, 'PUT', ballot, true);
  if (response.ok) {
    alert('Vote Casted');
    redirect('/');
  } else {
    alert('Error occured - recheck the data entered');
  }
}
