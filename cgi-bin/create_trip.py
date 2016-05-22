#!/usr/bin/python3
# -*- coding: utf-8 -*-
import html
import cgi
import sqlite3 as lite
import json
#import cgitb
import http.cookies
import os
#cgitb.enable()

import sys
import codecs
sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

form = cgi.FieldStorage()
name = html.escape(form.getfirst('name'))
date_start = html.escape(form.getfirst('date_start'))
date_end = html.escape(form.getfirst('date_end'))

cookie = http.cookies.SimpleCookie(os.environ.get('HTTP_COOKIE'))
login = cookie.get('login')

'''
try:
	#sys.stderr.write('sdfsdf')
except Exception as e:
	sys.stderr.write(str(e.args[1]))
'''

try:
	con = lite.connect('/home/CS/kashin_e_d/public_html/travel.db')
	cur = con.cursor()
	cur.execute("SELECT user_id FROM user where login=?", (login.value,))
	user_id = cur.fetchone()[0]
	cur.execute("INSERT INTO trip VALUES (?, ?, ?, ?)", (None, name, date_start, date_end)) #cur.lastrowid
	con.commit()
	trip_id = cur.lastrowid
	cur.execute("INSERT INTO user_trip VALUES(?, ?)", (user_id, trip_id))
	con.commit()
	trip = {'link': 'trip.py?id=' + str(trip_id), 'name': name}
	print("Status Code: 200")
	print("Content-type: text\n")
	print(json.dumps(trip))
except lite.Error:
	if con:
		con.rollback()
		print("Status Code: 201")
		print("Content-type: json\n")
		print('{"error": "Wrong trip name!"}')
		sys.exit(1)
finally:
	if con:
		con.close()