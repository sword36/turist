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

form = cgi.FieldStorage()
path_id = html.escape(form.getfirst('id'))
try:
	con = lite.connect('/home/CS/kashin_e_d/public_html/travel.db')
	cur = con.cursor()
	cur.execute("SELECT name, speed_mean, total_time, distance, speed_str,\
		time_str, date FROM path WHERE path_id=?", (path_id,))
	row = cur.fetchone()
	print("Status Code: 200")
	print("Content-type: text/html;charset=utf-8\n")
	print(templater.render_html_page('path', {'name': row[0],\
		'speed_mean': row[1], 'total_time': row[2], 'distance': row[3], 'speed_str': row[4],\
		'time_str': row[5], 'date': row[6]}))
except lite.Error:
	print("Status Code: 201\n")
	sys.exit(1)
finally:
	if con:
		con.close()