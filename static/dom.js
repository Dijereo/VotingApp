function appendNode(tag, className, parent=null, args={}) {
  let node = document.createElement(tag);
  node.className = className;
  if (parent) parent.appendChild(node);
  if (args.text) node.appendChild(document.createTextNode(args.text));
  if (args.type) node.type = args.type;
  if (args.value) node.value = args.value;
  if (args.checked) node.checked = args.checked;
  if (args.onclick) node.onclick = args.onclick;
  return node;
}

function appendRemoveButton(parent, onclick) {
  return appendNode('button', 'remove-button', parent,
    {text: '-', type: 'button', onclick: onclick});
}

function removeOnClick(button) {
  button.parentNode.parentNode.removeChild(button.parentNode);
}

function appendAddButton(parent, onclick) {
  return appendNode('button', 'add-button', parent,
    {text: '+', type: 'button', onclick: onclick});
}

function addPosition() {
  let positionFieldset = document.querySelector('#positions');
  positionFieldset.appendChild(createPositionDOM(newPosition()));
}

function addCandidate(candListDiv, name) {
  let candDiv = appendNode('div', 'cand-div', candListDiv);
  appendRemoveButton(candDiv, function(){removeOnClick(this)});
  appendNode('input', 'cand-input', candDiv, {type: 'text', value: name});
}

function addUser() {
  let userFieldset = document.querySelector('#users');
  userFieldset.appendChild(createUserDOM(newUser()));
}

function createPositionDOM(position) {
  let posDiv = appendNode('div', 'pos-div');
  appendRemoveButton(posDiv, function(){removeOnClick(this)});
  let titleDiv = appendNode('div', 'title-div', posDiv);
  appendNode('label', 'title-label', titleDiv, {text: 'Position Title'});
  appendNode('input', 'title-input', titleDiv, {type: 'text', value: position.title});
  let candListDiv = appendNode('div', 'cand-list-div', posDiv);
  appendNode('label', 'cand-label', candListDiv, {text: 'Candidates'});
  appendAddButton(candListDiv, function(){addCandidate(this.parentNode, '')});
  for (let candidate of position.candidates) {
    addCandidate(candListDiv, candidate.name);
  }
  return posDiv;
}

function createUserDOM(user) {
  let userDiv = appendNode('div', 'user-div');
  appendRemoveButton(userDiv, function(){removeOnClick(this)});
  let emailDiv = appendNode('div', 'email-div', userDiv);
  appendNode('label', 'email-label', emailDiv, {text: 'Email'});
  appendNode('input', 'email-input', emailDiv, {type: 'email', value: user.email});
  let voterDiv = appendNode('div', 'voter-div', userDiv);
  appendNode('label', 'voter-label', voterDiv, {text: 'Voter'});
  appendNode('input', 'voter-input', voterDiv, {type: 'checkbox', checked: user.isVoter});
  let adminDiv = appendNode('div', 'admin-div', userDiv);
  appendNode('label', 'admin-label', adminDiv, {text: 'Admin'});
  appendNode('input', 'admin-input', adminDiv, {type: 'checkbox', checked: user.isAdmin});
  return userDiv;
}

function getLocalISODate(date) {
  let tz = date.getTimezoneOffset();
  let local = date - tz * 60 * 1000;
  return (new Date(local)).toISOString().slice(0, 16);
}

function renderElectionData(electionData, formId) {
  let form = document.forms[formId];
  form['election'].value = electionData.election;
  let positionFieldset = document.querySelector('#positions');
  appendAddButton(positionFieldset, function(){addPosition()});
  for (let position of electionData.positions) {
    positionFieldset.appendChild(createPositionDOM(position));
  }
  let userFieldset = document.querySelector('#users');
  appendAddButton(userFieldset, function(){addUser()});
  for (let user of electionData.users) {
    userFieldset.appendChild(createUserDOM(user));
  }
  form['open-time'].value = getLocalISODate(new Date(electionData.openTime));
  form['close-time'].value = getLocalISODate(new Date(electionData.closeTime));
  form['expire-time'].value = getLocalISODate(new Date(electionData.expireTime));
}
