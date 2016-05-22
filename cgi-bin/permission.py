import sqlite3 as lite

def check_authorization(login, password):
	if login and password and login.value and password.value:
		con = lite.connect('/home/CS/kashin_e_d/public_html/travel.db')
		with con:
			cur = con.cursor()
			cur.execute("SELECT login, password FROM user WHERE login=?", (login.value,))
			row = cur.fetchone()
			if row:
				if password.value == row[1]:
					return True
	return False

def check_participation(login, trip_id):
	if login.value and trip_id:
		con = lite.connect('/home/CS/kashin_e_d/public_html/travel.db')
		with con:
			cur = con.cursor()
			cur.execute("SELECT * FROM user, user_trip WHERE\
				user.login=? AND user.user_id=user_trip.user_id AND\
				user_trip.trip_id=?", (login.value, trip_id))
			row = cur.fetchall()
			if row:
				if len(row) > 0:
					return True
	return False