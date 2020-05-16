let mockElection = {
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
  ],
  'users': [
    {
      'email': 'some.email@domain.com',
      'isVoter': true,
      'isAdmin': true
    }
  ],
  openTime: Date.now(),
  closeTime: Date.now(),
  expireTime: Date.now()
};

function convertElectionData(electionData) {
  for (let user of electionData.users) {
    user.isVoter = user.is_voter;
    user.isAdmin = user.is_admin;
  }
  electionData.openTime = electionData.open_time * 1000;
  electionData.closeTime = electionData.close_time * 1000;
  electionData.expireTime = electionData.expire_time * 1000;
  return electionData;
}

async function getElectionData() {
  let electionId = localStorage.getItem(electionIdLookup);
  let response = await sendRequest(
    `/edit/${electionId}`, 'GET', null, true
  );
  if (response.ok) {
    let electionData = await response.json();
    electionData = convertElectionData(electionData);
    console.log(electionData);
    return electionData;
  }
  return null;
}

async function editElection(electionData) {
  let electionId = localStorage.getItem(electionIdLookup);
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
