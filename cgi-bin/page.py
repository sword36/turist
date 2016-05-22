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
page_login = login.value
try:
	page_login = html.escape(form.getfirst('login'))
except Exception:
	pass
con = lite.connect('/home/CS/kashin_e_d/public_html/travel.db')
with con:
	cur = con.cursor()
	cur.execute("SELECT user_id, login, password FROM user WHERE login=?", (page_login,))
	row = cur.fetchone()
	print("Status Code: 200")
	print("Content-type: text/html;charset=utf-8\n")
	print(templater.render_html_page('homepage', {'user_id': row[0],\
		'login': row[1]}))
	sys.exit(1)
print("Status Code: 200")
print("Content-type: text/html;charset=utf-8\n")