#!/usr/bin/python3
# -*- coding: utf-8 -*-
import cgi
import sys
import codecs
sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
#sys.stderr.write(str(sys.stdin.read()))
form = cgi.FieldStorage(keep_blank_values=1)
import html
#import sys
import sqlite3 as lite
import json
import permission
import http.cookies
import os
import nmea_parser

cookie = http.cookies.SimpleCookie(os.environ.get('HTTP_COOKIE'))
login = cookie.get('login')

'''
try:
	sys.stderr.write(str(form.keys()))
except Exception as e:
	sys.stderr.write(str(e.args[1]))
'''
name = html.escape(form.getfirst('name'))
trip_id = html.escape(form.getfirst('trip_id'))

is_participation = permission.check_participation(login, trip_id)
if not is_participation:
		print("Status Code: 201")
		print("Content-type: json\n")
		print('{"error": "You not participate in this trip!"}')
		sys.exit(10)
file_item = form['file']
if file_item.file:
	raw_data = file_item.file.readlines() #open('../temp/' + fn).readlines()
	raw_data = list(map(lambda x: x.decode('utf-8'), raw_data))
try:
	con = lite.connect('/home/CS/kashin_e_d/public_html/travel.db')
	cur = con.cursor()

	cur.execute("SELECT * FROM path WHERE trip_id=? AND name=?", (trip_id, name))
	same_path = cur.fetchone();
	if same_path:
		print("Status Code: 201")
		print("Content-type: json\n")
		print('{"error": "Wrong path name!"}')
		sys.exit(2)
	stats = None
	try:
		stats = nmea_parser.get_stats(raw_data)
		sys.stderr.write(str(stats))
	except Exception as e:
		print("Status Code: 200")
		print("Content-type: json\n")
		print(json.dumps({'error': 'Wrong file format: %s' % str(e.args)}))
		sys.exit(1)
	cur.execute("INSERT INTO path VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (None, name, '\n'.join(raw_data), stats['speed_mean'],\
		stats['total_time'], stats['distance'], stats['speed_str'], stats['time_str'], stats['date'], trip_id))
	con.commit()
	trip = {'link': 'path.py?id=' + str(cur.lastrowid), 'name': name}
	print("Status Code: 200")
	print("Content-type: json\n")
	print(json.dumps(trip))
except lite.Error as e:
	if con:
		con.rollback()
		print("Status Code: 201")
		print("Content-type: json\n")
		print(json.dumps({'error': str(e.args)}))
		sys.exit(3)
finally:
	if con:
		con.close()