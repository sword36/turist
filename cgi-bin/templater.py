#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys
import codecs
sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

_templates = {'login':'''<div class='jumbotron'>
<h2>Дневник туриста. Добро пожаловать.</h2>
</div>
<form action="./authorize.py" method='POST' onsubmit='checkLogin()' class='text-center'>
<div class='form-group'>
<input name="login" placeholder='Логин' id='login' required autofocus>
</div>
<div class='form-group'>
<input name="password" type='password' id='password' placeholder='Пароль' required>
</div>
<button type="submit" class='btn btn-success'>Вход</button>''',

'login_failed':'''<div class='jumbotron'>
<h2>Добро пожаловать</h2>
</div>
<div class='alert alert-danger text-center'>
<h3>Неверный логин или пароль!</h3>
</div>
<form action="./authorize.py" method='POST' onsubmit='checkLogin()' class='text-center'>
<div class='form-group'>
<input name="login" placeholder='Логин' id='login' required autofocus>
</div>
<div class='form-group'>
<input name="password" type='password' id='password' placeholder='Пароль' required>
</div>
<button type="submit" class='btn btn-success'>Вход</button>''',

'homepage':'''<div class='jumbotron'>
<h2>Страница туриста</h2>
</div>
<div class='well'>
<h4>
<p>Id: {user_id}</p>
<p>Логин: {login}</p>
</h4>
</div>
<div class='row'>
<div class='col-lg-6'>
<h3>Участие в путешествиях:</h3>
<ul id='trips'></ul>
</div>
<div class='col-lg-6'>
<h3>Поиск по путешествиям</h3>
<form action='search.py' method='POST' class='navbar-form'>
<div class='form-group'>
<input name='trip' class='form-control'>
</div>
<button type='submit' class='btn btn-success'>Найти</button>
</form>
</div>
</div>

<div>
<form id='createTripForm' method='POST' class='navbar-form navbar-fixed-bottom text-center' onsubmit='createTrip()'>
<div class='form-group'>
<input id='tripName' class='form-control'>
</div>
<div class='form-group'>
<input type='date' id='dateStart' class='form-control' required>
</div>
<div class='form-group'>
<input type='date' id='dateEnd' class='form-control' required>
</div>
<button type='submit' class='btn btn-success' id='createTripBtn'>Создать путешествие</button>
</form>
</div>
<script>
showLoginTrips();
</script>''',

'trip': '''
<div class='jumbotron'>
<h2>Путешествие: {name}</h2>
<button id='tripStatusBtn' class='btn btn-primary' data-status={trip_status} onclick='changeTripStatus();'>{trip_status_text}</button><br>
</div>
<div class='well'>
<h4>
<p>Время начала: {date_start}</p>
<p>Время конца: {date_end}<br></p>
</h4>
</div>
<div class='row'>
<div class='col-lg-6'>
<h3>Пути:</h3>
<ul id='paths'></ul>
</div>
<div class='col-lg-6'>
<h3>Участники:</h3>
<ul id='users'></ul>
</div>
</div>
<div>
<form id='createPathForm' method='POST' class='navbar-form navbar-fixed-bottom text-center' onsubmit='createPath()'>
<div class='form-group'>
<input id='pathName' class='form-control' required>
</div>
<div class='form-group'>
<input type='file' id='data' class='form-control' required>
</div>
<button type='submit' class='btn btn-success'>Добавить путь</button>
</form>
</div>
<script>
showPaths();
</script>
''',

'path': '''
<div class='jumbotron'>
<h2>Путь: {name}</h2>
</div>
<div class='well'>
<p>Средняя скорость: {speed_mean} км/ч</p>
<p>Общее время: {total_time} сек</p>
<p>Пройденное расстояние: {distance} метров</p>
<p>Время старта: {date}</p>
<p><div style="width: 60%; height:50%;" class='text-center'>
<canvas id="pathChart"></canvas></p>
</div>
</div>
<script>drawChart('{speed_str}', '{time_str}');</script>
''',

'search': '''<button id='home' onclick='goHome()'>Моя страница</button>
<div class='jumbotron'>
<h2>Поиск по путешествиям</h2>
</div>
<form onsubmit='showNameTrips()' method='POST' class='navbar-form'>
<div class='form-group'>
<input id='tripName' value='{trip_name}' onkeyup='showNameTrips()' class='form-control' autocomplete='off'>
</div>
<button type='submit' class='btn btn-success'>Найти</button>
</form>
<div id='trips'>
</div>
<script>showNameTrips()</script>'''
}

_layout_before = '''<html>
<head>
<meta charset="utf-8">
<title>{0}</title>
<link href="../css/bootstrap.min.css" rel="stylesheet">
<script src='../js/jquery.min.js'></script>
<script src='../js/bootstrap.min.js'></script>
<script src='../js/chart.js'></script>
<script src='../js/main.js'></script>
</head>
<body>
<div class='container'>'''

_layout_before_authorized = '''
<nav class='navbar navbar-inverse navbar-fixed-top'>
<div class='container'>
<div class='navbar-header'>
<div class='navbar-brand'>
<button id='home' onclick='goHome()' class='btn btn-primary'>Моя страница</button>
</div>
</div>
<div class='navbar-right'>
<div class='navbar-brand'>
<form action='exit.py' method='POST'>
<button id='exit' type='submit' class='btn btn-primary'>Выйти</button>
</form>
</div>
</div>
</div>
</nav>
'''

_layout_after = '''
</div>
</body>
</html>'''

def render_html_page(name, params=None):
	tmpl = _templates.get(name, 'login')
	if params:
		tmpl = tmpl.format(**params)
	if name == 'login' or name == 'login_failed':
		return _layout_before.format(name) + tmpl + _layout_after
	else:
		return _layout_before.format(name) + _layout_before_authorized + tmpl + _layout_after



def make_html_page(name, tmpl):
	return _layout_before.format(name) + tmpl + _layout_after

def redirect(url):
	return '''
	<html><body><script>document.location='{0}'</script></body></html>'''.format(url)
