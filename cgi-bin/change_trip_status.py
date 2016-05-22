#!/usr/bin/python3
# -*- coding: utf-8 -*-
import html
import cgi
import sqlite3 as lite
import json
import cgitb
import http.cookies
import os
cgitb.enable()

import sys
import codecs
sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

form = cgi.FieldStorage()
status = html.escape(form.getfirst('status'))
trip_id = html.escape(form.getfirst('trip_id'))
cookie = http.cookies.SimpleCookie(os.environ.get('HTTP_COOKIE'))
login = cookie.get('login')

text = {'in': 'Выйти из путешествия', 'out': 'Вступить в путешествие'}

try:
	con = lite.connect('/home/CS/kashin_e_d/public_html/travel.db')
	cur = con.cursor()
	cur.execute("SELECT user_id FROM user WHERE login=?", (login.value,))
	user_id = cur.fetchone()[0]
	if status == 'in':
		cur.execute("DELETE FROM user_trip WHERE user_id=? AND trip_id=?", (user_id, trip_id))
		con.commit()
		status = 'out'
	elif status == 'out':
		cur.execute("INSERT INTO user_trip VALUES (?, ?)", (user_id, trip_id))
		con.commit()
		status = 'in'
	else:
		print("Status Code: 201")
		print("Content-type: json\n")
		print(json.dumps({'error': str(e.args[0])}))
		sys.exit(1)
	print("Content-type: json\n")
	print(json.dumps({'status': status, 'text': text[status]}))
except lite.Error as e:
	if con:
		con.rollback()
		print("Status Code: 201")
		print("Content-type: json\n")
		print(json.dumps({'error': str(e.args[0])}))
	sys.exit(1)
finally:
	if con:
		con.close()