let mockResults = {
  'election': 'Mock Election',
  'positions': [
    { 'title': 'President',
      'candidates': [
        {'name': 'John Doe', 'votes': 7},
        {'name': 'Mary Sue', 'votes': 5}
      ]
    },
    { 'title': 'Vice President',
      'candidates': [
        {'name': 'Joe Bob', 'votes': 4},
        {'name': 'No Confidence', 'votes': 6}
      ]
    }
  ]
};

async function getResults() {
  let electionId = sessionStorage.getItem(electionIdLookup);
  let response = await sendRequest(`/results/${electionId}`, 'GET', null, true);
  if (response.ok) {
    let result = await response.json();
    return result;
  } else {
    return null;
  }
}

function loadResults(electionData) {
  if (electionData === null) {
    alert('Cannot access results');
    redirect('/');
  }
  document.querySelector('#election').innerHTML = electionData.election;
  let resultsHTML = "";
  for (let position of electionData.positions) {
    resultsHTML += `<h3>${position.title}</h3><table>`;
    for (let candidate of position.candidates) {
      resultsHTML += `<tr><td>${candidate.name}</td><td>${candidate.votes}</td></tr>`;
    }
    resultsHTML += `</table>`;
  }
  let resultsDiv = document.querySelector('#results');
  resultsDiv.innerHTML = resultsHTML;
}
