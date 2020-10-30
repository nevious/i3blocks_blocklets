#!/usr/bin/env python3

# MIT License

# Copyright (c) 2020 Christian Schläppi

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import sys
import fcntl
import array
import socket
import json
import struct
import pprint

def get_default_route_interface():
	fd = open('/proc/net/route', 'r')
	# field mapping; head -n 1 /proc/net/route
	# Iface Destination Gateway ...
	# only interested in the first three
	routes = [entry.split('\t')[:3] for entry in fd.readlines()[1:]]
	fd.close()

	for route in enumerate(routes):
		if int(route[1][2], 16) == 0:
			return route[1][0]

	return None

def if_wifi_and_signal_ind(iface):
	fd = open('/proc/net/wireless', 'r')

	for record in fd.readlines():
		record = record.split()
		if record[0][:-1] == iface: # remove colon at end of interface name
			return (True, record[2])

	return (False, None)

def get_wifi_name(iface):
	"""
	based on https://stackoverflow.com/questions/14142014/how-can-i-get-the-active-essid-on-an-interface
	"""
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	essid = array.array('b', [ord(i) for i in '\0' * 32])  # define 32b array to store the name
	essid_pointer, essid_length = essid.buffer_info()
	ioctl_request = array.array(
		'b',
		iface.ljust(16, '\0').encode() +
		struct.pack("PHH", essid_pointer, essid_length, 0)
	)
	# linux/wireless.h
	# #define SIOCGIWESSID    0x8B1B          /* get ESSID */
	fcntl.ioctl(sock.fileno(), 0x8B1B, ioctl_request)

	return essid.tobytes().decode().rstrip('\0')

def get_if_address(iface):
	"""
	based on https://stackoverflow.com/questions/6243276/how-to-get-the-physical-interface-ip-address-from-an-interface

	get_wifi_name might be very overcomplicated when looking at this...
	"""
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	# linux/sockios.h
	# define SIOCGIFADDR     0x8915          /* get PA address               */
	raw_ifaddr = fcntl.ioctl(
		sock.fileno(),
		0x8915,
		struct.pack('256s', iface[:15].encode())
	)[20:24]

	return socket.inet_ntoa(raw_ifaddr)

def generate_signal_color(indicator):
	indicator = int(indicator)

	color_map = {
		'high': '#66C635',
		'mid': '#ACC736',
		'low': '#C77236'
	}

	# based on 70 == 100% = this is how iwconfig reports link quality
	# 56 == 80%, 21 == 30%
	if indicator >= 56:
		return color_map['high']
	if 57 >= indicator <= 21:
		return color_map['mid']
	
	return color_map['low']


def print_output(is_wifi, signal_indicator, iface, ssid, if_addr):

	template = {
		'wired': {
			'full_text': "<span foreground='{}'>: {}</span>"
		},
		'wireless': {
			'full_text': "  {0}:{1} <span foreground='{2}'> {3:.0f}%</span>"
		},
		'none': {
			'full_text': '<span foreground="{0}"> down</span>'
		}
	}

	if signal_indicator and signal_indicator.endswith('.'):
		signal_indicator = signal_indicator[:-1]

	if not iface:
		print(template['none']['full_text'].format('#C74936'))
	elif is_wifi:
		print(template['wireless']['full_text'].format(
				ssid,
				if_addr,
				generate_signal_color(signal_indicator),
				int(signal_indicator)*100/70
			)
		)
	elif not is_wifi and if_addr:
		print(template['wired']['full_text'].format('#FFFFFF'))

def main():
	iface = get_default_route_interface()
	
	if not iface:
		print_output(None, None, None, None, None)
		sys.exit(0)

	wifi, signal_indicator = if_wifi_and_signal_ind(iface)
	ssid = None

	if wifi and signal_indicator:
		ssid = get_wifi_name(iface)

	if_addr = get_if_address(iface)
	
	print_output(wifi, signal_indicator, iface, ssid, if_addr)

if __name__ == '__main__':
	main()
