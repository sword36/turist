#!/usr/bin/python3
# -*- coding: utf-8 -*-
import cgi, sys, os
import cgitb; cgitb.enable()
import html
import sqlite3 as lite
import templater
import permission
import http.cookies

cookie = http.cookies.SimpleCookie(os.environ.get('HTTP_COOKIE'))
login = cookie.get('login')
password = cookie.get('password')

isAuthorize = permission.check_authorization(login, password)
if not isAuthorize:
	print("Status Code: 200")
	print("Content-type: text/html;charset=utf-8\n")
	print(templater.redirect('login.py'))
	sys.exit(1)

text = {'in': 'Выйти из путешествия', 'out': 'Вступить в путешествие'}

form = cgi.FieldStorage()
trip_id = html.escape(form.getfirst('id'))
try:
	con = lite.connect('/home/CS/kashin_e_d/public_html/travel.db')
	cur = con.cursor()
	cur.execute("SELECT name, date_start, date_end FROM trip WHERE trip_id=?", (trip_id,))
	row = cur.fetchone()
	cur.execute("SELECT * FROM user, user_trip WHERE user.login=? \
		AND user.user_id=user_trip.user_id AND user_trip.trip_id=?", (login.value, trip_id))
	trip_status = 'in'
	if cur.fetchone():
		trip_status = 'in'
	else:
		trip_status = 'out'
	trip_status_text = text[trip_status]
	print("Status Code: 200")
	print("Content-Type: text/html; charset=utf-8\n")
	print(templater.render_html_page('trip', {'name': row[0],\
		'date_start': row[1], 'date_end': row[2], 'trip_status': trip_status, 'trip_status_text': trip_status_text}))
except lite.Error as e:
	print("Status Code: " + str(e.args[0])  + "\n")
	sys.exit(1)
finally:
	if con:
		con.close()