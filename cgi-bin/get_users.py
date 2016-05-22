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

form = cgi.FieldStorage()
trip_id = None
try:
	trip_id = html.escape(form.getfirst('trip'))
except:
	pass

try:
	con = lite.connect('/home/CS/kashin_e_d/public_html/travel.db')
	cur = con.cursor()
	cur.execute("SELECT user.login FROM user_trip, user WHERE user_trip.trip_id=? AND \
		user_trip.user_id=user.user_id", (trip_id,))
	rows = cur.fetchall()
	users = []
	for row in rows:
		users.append({'link': 'page.py?login=' + str(row[0]), 'name': row[0]})
	print("Status Code: 200")
	print("Content-type: json\n")
	print(json.dumps(users))
except lite.Error:
	print("Status Code: 201\n")
	sys.exit(1)
finally:
	if con:
		con.close()