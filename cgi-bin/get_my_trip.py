#!/usr/bin/python3
# -*- coding: utf-8 -*-
import html
import cgi
import sqlite3 as lite
import json
import cgitb
import permission
import http.cookies
import os
cgitb.enable()

import sys
import codecs
sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

cookie = http.cookies.SimpleCookie(os.environ.get('HTTP_COOKIE'))
login = cookie.get('login')

form = cgi.FieldStorage()
trip_name = None
try:
	trip_name = html.escape(form.getfirst('trip'))
except:
	pass

try:
	con = lite.connect('/home/CS/kashin_e_d/public_html/travel.db')
	cur = con.cursor()
	if trip_name:
		trip_name += '%'
		cur.execute("SELECT trip_id, name FROM trip WHERE name LIKE :trip_name", (trip_name,))
	else:
		cur.execute("SELECT trip.trip_id, trip.name FROM user, user_trip, trip\
			WHERE user.login=? AND user.user_id=user_trip.user_id AND user_trip.trip_id=trip.trip_id",
			(login.value,))
	rows = cur.fetchall()
	trips = []
	for row in rows:
		trips.append({'link': 'trip.py?id=' + str(row[0]), 'name': row[1]})
	print("Status Code: 200")
	print("Content-type: json\n")
	print(json.dumps(trips))
except lite.Error:
	print("Status Code: 201\n")
	sys.exit(1)
finally:
	if con:
		con.close()