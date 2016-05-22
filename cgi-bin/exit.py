#!/usr/bin/python3
# -*- coding: utf-8 -*-
import html
import cgi
import sqlite3 as lite
import json
import sys
import cgitb
import permission
import http.cookies
import os
import templater
cgitb.enable()

print("Set-cookie:login=''; httponly")
print("Set-cookie:password=''; httponly")
print("Content-type: text/html\n")
print(templater.redirect('login.py'))