#!/usr/bin/python3
# -*- coding: utf-8 -*-
import cgi, os, sys
import cgitb; cgitb.enable()
import templater

form = cgi.FieldStorage()
error = None
print("Status Code: 200")
print("Content-type: text/html;charset=utf-8\n")
error = form.getfirst('error')
if not error:
	print(templater.render_html_page('login'))
else:
	print(templater.render_html_page('login_failed'))
