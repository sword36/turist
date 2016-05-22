#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sqlite3 as lite

def check(login, password):
	if login:
		con = lite.connect('/home/CS/kashin_e_d/public_html/travel.db')
		with con:
			cur = con.cursor()
			cur.execute("SELECT login, password FROM user WHERE login=?", (login,))
			row = cur.fetchone()
			if row:
				if password == row[1]:
					return True
	return False