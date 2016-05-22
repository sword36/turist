#!/usr/bin/python3
# -*- coding: utf-8 -*-
import re
import operator
from functools import reduce
from datetime import date
import datetime

def timestamp(s):
    ms_s = s[6:]
    ms = ms_s and int(float(ms_s) * 1000000) or 0

    t = datetime.time(
        hour=int(s[0:2]),
        minute=int(s[2:4]),
        second=int(s[4:6]),
        microsecond=int(ms))
    return t


sentence_re = re.compile(r'''
        # start of string, optional whitespace, optional '$'
        ^\s*\$?

        # message (from '$' or start to checksum or end, non-inclusve)
        (?P<nmea_str>
            # sentence type identifier
            (?P<sentence_type>

                # proprietary sentence
                (P\w{3})|

                # query sentence, ie: 'CCGPQ,GGA'
                # NOTE: this should have no data
                (\w{2}\w{2}Q,\w{3})|

                # taker sentence, ie: 'GPGGA'
                (\w{2}\w{3},)
            )

            # rest of message
            (?P<data>[^*]*)

        )
        # checksum: *HH
        (?:[*](?P<checksum>[A-F0-9]{2}))?

        # optional trailing whitespace
        \s*[\r\n]*$
        ''', re.X | re.IGNORECASE)

def checksum(nmea_str):
	return reduce(operator.xor, map(ord, nmea_str))

def parse(line):
	match = sentence_re.match(line)
	if not match:
		raise ValueError('could not parse data: %r' % line)
	nmea_str = match.group('nmea_str')
	data_str = match.group('data')
	sentence_type = match.group('sentence_type').upper()
	data = data_str.split(',')
	check = match.group('checksum')

	if checksum:
		cs1 = int(check, 16)
		cs2 = checksum(nmea_str)
		if cs1 != cs2:
			raise Exception('Wrong checksum value!')
	return sentence_type, data

def get_GPRMC(data):
	gprmc = []
	for line in data:
		parsed_line = parse(line)
		if re.match('GPRMC', parsed_line[0]):
			gprmc.append(parsed_line[1])
	return gprmc

def mean(arr):
	return reduce(operator.add, arr) / len(arr)

def get_distance(speeds, times):
    distance = 0
    for i in range(1, len(times)):
        distance += speeds[i] * (times[i] - times[i - 1])
    distance *= 10/36 # from km/h to m/c
    #print('dist: ', distance)
    return distance 

def get_total_time(times):
    total_time = times[-1] - times[0]
    #print('total time: ', total_time)
    return total_time

def get_stats(data):
	gprmc = get_GPRMC(data)
	gprmc = list(filter(lambda x: x[6] != '', gprmc))
	speeds = [round(float(x[6]) * 1.852, 2) for x in gprmc]
	start_time = datetime.datetime.combine(date.today(), timestamp(gprmc[0][0]))
	times = [(datetime.datetime.combine(date.today(), timestamp(x[0])) - start_time).seconds \
		for x in gprmc]
	speed_mean = mean(speeds)
	distance = get_distance(speeds, times)
	total_time = get_total_time(times)
	date_start = ''
	i = 0
	while not date_start:
		date_start = gprmc[i][8]
		i += 1
	date_start = date_start[:2] + '.' + date_start[2:4] + '.' + date_start[4:6]
	speed_str = ','.join(map(lambda x: str(x), speeds))
	time_str = ','.join(map(str, times))
	return {
		'speed_mean': int(speed_mean),
		'total_time': total_time,
		'distance': int(distance),
		'date': date_start,
		'speed_str': speed_str,
		'time_str': time_str
	}