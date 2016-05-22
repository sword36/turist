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
login = cookie.get('login').value

form = cgi.FieldStorage()
try:
	login = html.escape(form.getfirst('login'))
except:
	pass

try:
	con = lite.connect('/home/CS/kashin_e_d/public_html/travel.db')
	cur = con.cursor()
	cur.execute("SELECT trip.trip_id, trip.name FROM user, user_trip, trip\
		WHERE user.login=? AND user.user_id=user_trip.user_id AND user_trip.trip_id=trip.trip_id",
		(login,))
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