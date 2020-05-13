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
