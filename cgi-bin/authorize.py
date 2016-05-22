#!/usr/bin/python3
# -*- coding: utf-8 -*-
import cgi
import cgitb; cgitb.enable()
import html
import sqlite3 as lite
import templater
import http.cookies
from urllib import parse

form = cgi.FieldStorage()
login = form.getfirst('login')
password = form.getfirst('password')

if (not login or not password):
	print("Status Code: 200")
	print("Content-type: text/html;charset=utf-8\n")
	print(templater.redirect('login.py?error=login'))
else:
	login = html.escape(login)
	password = html.escape(password)

con = lite.connect('/home/CS/kashin_e_d/public_html/travel.db')
with con:
	cur = con.cursor()
	cur.execute("SELECT user_id, login, password FROM user WHERE login=?", (login,))
	row = cur.fetchone()
	if row:
		if (row[2] == password): #success 
			print("Set-cookie:login=" + login + "; httponly")
			print("Set-cookie:password=" + password + "; httponly")
			#print("HTTP/1.1 301 Found")
			#print("Location: /cgi-bin/page%login=" + login + ";%password=" + password + '\n')
			print("Status Code: 200")
			print("Content-type: text/html;charset=utf-8\n")
			print(templater.redirect('page.py?login=' + login))
		else: # wrong password
			print("Status Code: 200")
			print("Content-type: text/html;charset=utf-8\n")
			print(templater.redirect('login.py?error=login'))
	else: #new user
		cur.execute("INSERT INTO user VALUES(null, ?, ?)", (login, password))
		print("Set-cookie:login=" + login + "; httponly")
		print("Set-cookie:password=" + password + "; httponly")
		print("Status Code: 200")
		print("Content-type: text/html;charset=utf-8\n")
		print(templater.redirect('page.py?login=' + login))