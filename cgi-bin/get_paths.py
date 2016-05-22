#!/usr/bin/python3
# -*- coding: utf-8 -*-
import html
import cgi
import sqlite3 as lite
import json
import os
import cgitb
cgitb.enable()

import sys
import codecs
sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

form = cgi.FieldStorage()
trip_id = None
try:
	trip_id = html.escape(form.getfirst('trip'))
except:
	pass
try:
	con = lite.connect('/home/CS/kashin_e_d/public_html/travel.db')
	cur = con.cursor()
	cur.execute("SELECT path_id, name FROM path\
	 WHERE trip_id=?", (trip_id,))
	rows = cur.fetchall()
	paths = []
	for row in rows:
		paths.append({'link': 'path.py?id=' + str(row[0]), 'name': row[1]})
	print("Status Code: 200")
	print("Content-type: json\n")
	print(json.dumps(paths))
except lite.Error:
	print("Status Code: 201\n")
	sys.exit(1)
finally:
	if con:
		con.close()