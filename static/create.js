let emptyData = {
  election: '', positions: [], users: [],
  openTime: Date.now(), closeTime: Date.now(), expireTime: Date.now()
};

async function postElection(electionData) {
  let response = await sendRequest('/create', 'POST', electionData, false);
  if (response.ok) {
    alert('Election created');
    redirect('/');
  } else {
    alert('Error occured - recheck the data entered');
  }
}
