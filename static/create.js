async function postElection(formId, electionData) {
  let response = await sendRequest('/create', 'POST', electionData, false);
  if (response.ok) {
    alert('Election created');
    redirect('/');
  } else {
    alert('Error occured - recheck the data entered');
  }
}
