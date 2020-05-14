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
  let response = await sendRequest(
    `${host}/vote/${electionId}`,
    'GET', null, true
  );
  if (response.ok) {
    let result = await response.json();
    return result;
  }
  return null;
}

function loadBallot(electionData) {
  if (electionData === null) {
    alert('Cannot access election');
    redirect('/');
  }
  document.querySelector('#election').innerHTML = electionData.election;
  let resultsDiv = document.querySelector('#ballot');
  resultsDiv.innerHTML = "";
  resultsDiv.innerHTML = `<form id="vote-form"></form>`;
  for (let position of electionData.positions) {
    resultsDiv.innerHTML += `<h3>${position.title}</h3>`;
    for (let candidate of position.candidates) {
      resultsDiv.innerHTML += `<label for="${candidate.name}">${candidate.name}</label>`
      resultsDiv.innerHTML += `<input type="radio" id="${candidate.name}" value="${candidate.name}"/>`;
    }
  }  
  resultsDiv.innerHTML += `<button type="button" onclick="castVote(getBallotData('vote-form'))">Vote</button>`;
  resultsDiv.innerHTML += `</form>`;
}

function getBallotData(formId) {
  let form = document.forms[formId];
  // TODO
}

async function castVote(ballot) {
  let electionId = sessionStorage.getItem(electionIdLookup);
  let response = await sendRequest(`/vote/${electionId}`, 'PUT', ballot, true);
  if (response.ok) {
    alert('Election createdVote Cast');
    redirect('/');
  } else {
    alert('Error occured - recheck the data entered');
  }
}
