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
    alert("Cannot access results");
    redirect("/");
  }
  let election = electionData.election;
  document.querySelector("#election").innerHTML = electionData.election;
  let resultsHTML = "";
  let resultsDiv = document.querySelector("#results");

  var titArr = [];
  var nameArr = [];
  var voteArr = [];
  var voteComp = 0;
  var objArr = [];
  for (let position of electionData.positions) {
    resultsHTML += `<h3>${position.title}</h3><table>`;
    titArr.push(position.title);
    for (let candidate of position.candidates) {
      resultsHTML += `<tr><td>${candidate.name}</td><td>${candidate.votes}</td></tr>`;
      if (Number(candidate.votes) > voteComp) {
        var voteMin = new Object();
        voteMin.vote = candidate.votes;
        voteMin.name = candidate.name;
        voteComp = voteMin.vote;
      }
      //console.log(voteMin.vote);
      //console.log(voteMin.name);
    }
    nameArr.push(voteMin.name);
    voteArr.push(voteMin.vote);
    resultsHTML += `</table>`;

    pairObj = position.title + ": " + voteMin.name;
    objArr.push(pairObj);

    voteComp = 0;
    //var objArr = [];
  }
  resultsDiv.innerHTML = resultsHTML;
  resultsHTML += `<script>${drawChart(objArr, voteArr, election)}</script>`;
  //console.log(titArr);
  //console.log(nameArr);
  //console.log(voteArr);
  //console.log(election);
}

function drawChart(pairObj, voteArr, election) {
  var myChart = Highcharts.chart("container", {
    chart: {
      type: "bar",
    },
    title: {
      text: election,
    },
    xAxis: {
      categories: pairObj,
    },
    yAxis: {
      title: {
        text: "Votes Obtained",
      },
    },
    series: [{ name: "Votes", data: voteArr }],
  });
}