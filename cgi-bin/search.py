#!/usr/bin/python3
# -*- coding: utf-8 -*-
import cgi, sys, os
import cgitb; cgitb.enable()
import html
import sqlite3 as lite
import templater
import permission
import http.cookies
from urllib import parse

import sys
sys.stderr = sys.stdout

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
trip_name = ''
try:
	trip_name = html.escape(form.getfirst('trip')) #html.escape(parse.unquote(form.getfirst('trip')).encode('utf-8'))
except Exception:
	pass
print("Status Code: 200")
print("Content-type: text/html;charset=utf-8\n")
#print(form.getfirst('trip'))
print(templater.render_html_page('search', {'trip_name': trip_name}))