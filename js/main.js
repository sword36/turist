function createTripRequest(name, dateStart, dateEnd, login) {
	xhr = new XMLHttpRequest();
	xhr.open('POST', 'create_trip.py'); //'GET', 'create_trip.py?name=' + name.value + 
		//'&date_start=' + dateStart.value + '&date_end=' + dateEnd.value +
		//'&login=' + login, true);
	var formData = new FormData();
	formData.append('name', name.value);
	formData.append('date_start', dateStart.value);
	formData.append('date_end', dateEnd.value);
	formData.append('login', login);
	xhr.send(formData);
	xhr.onreadystatechange = function() {
		if (xhr.readyState != 4) return;
		if (xhr.status == 200) {
			name.value = '';
			dateStart.value = '';
			dateEnd.value = '';
			var parsed = JSON.parse(xhr.response ? xhr.response : "{}");
			if ('error' in parsed) {
				alert(parsed['error']);
			} else {
				addTrip(parsed, '#trips');
			}
		}
	}
}

function createPathRequest(name, file, tripId) {
	xhr = new XMLHttpRequest();
	xhr.open('POST', 'create_path.py');
	var formData = new FormData();
	formData.append('file', file.files[0]);
	formData.append('name', name.value);
	formData.append('trip_id', tripId);
	xhr.send(formData);
	xhr.onreadystatechange = function() {
		if (xhr.readyState != 4) return;
		if (xhr.status == 200) {
			name.value = '';
			file.value = '';
			var parsed = JSON.parse(xhr.response ? xhr.response : "{}");
			if ('error' in parsed) {
				alert(parsed['error']);
			} else {
				addPath(parsed, '#paths');
			}
		}
	}
}

function createTrip() {
	event.preventDefault();
	var tripName = document.querySelector('#tripName');
	var dateStart = document.querySelector('#dateStart');
	var dateEnd = document.querySelector('#dateEnd');
	if (!tripName.value || !dateStart.value || !dateEnd.value) {
		alert('Please, input all inforamation about trip!');
		return false;
	}
	createTripRequest(tripName, dateStart, dateEnd, getLocation());
	return false;
}


function createPath() {
	event.preventDefault();
	var pathName = document.querySelector('#pathName');
	var data = document.querySelector('#data');
	if (!data.value || !pathName.value) {
		alert('Please, input all inforamation about path!');
		return false;
	}
	createPathRequest(pathName, data, getLocation());
	return false;
}

function loadTrips(name, value, cb) {
	xhr = new XMLHttpRequest();
	if (name == 'login') {
		xhr.open('POST', 'get_user_trips.py', true);
	} else {
		xhr.open('POST', 'get_trips.py', true);
	}
	var formData = new FormData();
	formData.append(name, value);
	xhr.send(formData);
	xhr.onreadystatechange = function() {
		if (xhr.readyState != 4) return;
		if (xhr.status == 200) {
			cb(JSON.parse(xhr.response ? xhr.response : "[]"));
		}
	}
}

function loadTripPaths(trip, cb) {
	xhr = new XMLHttpRequest();
	xhr.open('GET', 'get_paths.py?trip=' + trip, true);
	xhr.send();
	xhr.onreadystatechange = function() {
		if (xhr.readyState != 4) return;
		if (xhr.status == 200) {
			cb(JSON.parse(xhr.response ? xhr.response : "[]"));
			showUsers();
		}
	}
}

function loadTripUsers(trip, cb) {
	xhr = new XMLHttpRequest();
	xhr.open('GET', 'get_users.py?trip=' + trip, true);
	xhr.send();
	xhr.onreadystatechange = function() {
		if (xhr.readyState != 4) return;
		if (xhr.status == 200) {
			cb(JSON.parse(xhr.response ? xhr.response : "[]"));
		}
	}
}

function addTrips(name, value, selectorId) {
	var el = document.querySelector(selectorId);
	el.textContent = ''
	loadTrips(name, value, function(trips) {
		for (var i = 0; i < trips.length; i++) {
			var li = document.createElement('li')
			var a = document.createElement('a');
			a.href = trips[i].link;
			var name = document.createTextNode(trips[i].name);
			a.appendChild(name);
			li.appendChild(a)
			el.appendChild(li);
		}
	});
}

function addPaths(trip, selectorId) {
	var el = document.querySelector(selectorId);
	loadTripPaths(trip, function(paths) {
		for (var i = 0; i < paths.length; i++) {
			var li = document.createElement('li')
			var a = document.createElement('a');
			a.href = paths[i].link;
			var name = document.createTextNode(paths[i].name);
			a.appendChild(name);
			li.appendChild(a)
			el.appendChild(li);
		}
	});
}

function addUsers(trip, selectorId) {
	var el = document.querySelector(selectorId);
	el.textContent = '';
	loadTripUsers(trip, function(users) {
		for (var i = 0; i < users.length; i++) {
			var li = document.createElement('li')
			var a = document.createElement('a');
			a.href = users[i].link;
			var name = document.createTextNode(users[i].name);
			a.appendChild(name);
			li.appendChild(a)
			el.appendChild(li);
		}
	});
}

function addPath(path, selectorId) {
	var el = document.querySelector(selectorId);
	var li = document.createElement('li')
	var a = document.createElement('a');
	a.href = path.link;
	var name = document.createTextNode(path.name);
	a.appendChild(name);
	li.appendChild(a)
	el.appendChild(li);
}

function addTrip(trip, selectorId) {
	var el = document.querySelector(selectorId);
	var li = document.createElement('li')
	var a = document.createElement('a');
	a.href = trip.link;
	var name = document.createTextNode(trip.name);
	a.appendChild(name);
	li.appendChild(a)
	el.appendChild(li);
}

function getLocation() {
	var re = /\w*$/;
	return document.location.search.match(re)[0];
}

function showLoginTrips() {
	var login = getLocation();
	addTrips('login', login, '#trips')
}

var lastTripName = null;
function showNameTrips() {
	if (event)
		event.preventDefault();
	var tripName = document.querySelector('#tripName');
	if (tripName.value == lastTripName)
		return false;
	lastTripName = tripName.value;
	addTrips('trip', tripName.value, '#trips');
	return false;
}

function showPaths() {
	var trip = getLocation();
	addPaths(trip, '#paths')
}

function showUsers() {
	var trip = getLocation();
	addUsers(trip, '#users')
}


function changeTripStatus() {
	var btn = document.querySelector('#tripStatusBtn');
	var status = btn.getAttribute('data-status');
	var trip_id = getLocation();
	changeTripStatusRequest(status, trip_id, function(response) {
		if ('error' in response) {
			alert('Error, try again');
		} else {
			btn.setAttribute('data-status', response.status);
			btn.textContent = response.text;
			showUsers();
		}
	});
}

function changeTripStatusRequest(status, trip_id, cb) {
	xhr = new XMLHttpRequest();
	xhr.open('GET', 'change_trip_status.py?status=' + status + 
		'&trip_id=' + trip_id, true);
	xhr.send();
	xhr.onreadystatechange = function() {
		if (xhr.readyState != 4) return;
		if (xhr.status == 200) {
			cb(JSON.parse(xhr.response ? xhr.response : "{}"));
		}
	}
}

function redirect(url) {
	document.location = url
}

function goHome() {
	redirect('page.py')
}

function checkLogin() {
	login = document.querySelector("#login");
	password = document.querySelector("#password");
	var re = /^\w{4,}$/;
	if (re.test(login.value) && re.test(password.value)) {
		return true;
	} else {
		alert('Данные должны состоять из латинских букв, цифр, а также быть длиннее 4 символов');
		event.preventDefault();
		return false;
	}
}

function drawChart(rawSpeed, rawTime) {
	var ctx = document.querySelector('#pathChart');
	var parsedSpeed = rawSpeed.split(',').map(parseFloat);
	var parsedTime = rawTime.split(',').map(parseFloat);
	var data = {labels: parsedTime, datasets: [{label: 'путь', backgroundColor: "rgba(75,192,192,0.4)",
		data: parsedSpeed}]};
	var pathChart = new Chart(ctx, {
		type: 'line',
		data: data,
		options:{
			scales: {
				xAxes: [{
					ticks: {
						type: 'linear',
						maxTicksLimit: 20
					}
				}]
			}
		}
		/*
		options: {
    		scales: {
        		xAxes: [{
            		ticks: {
                		// Return an empty string to draw the tick line but hide the tick label
                		// Return `null` or `undefined` to hide the tick line entirely
                   		userCallback: function(value, index, values) {
                   			var x = Math.pow(10, String(values.length).length - 1)
                    		return (index % x == 0) ? value : '';
                		}
            		}
        		}]
    		}
		}*/
	});
}