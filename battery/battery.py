#!/usr/bin/python

# MIT License

# Copyright (c) 2017 Christian Schläppi

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
import psutil
import datetime

def main():
	output_map = {
		'b_high': ('', '#66c635'),
		'b_mid': ('', '#79d14d'),
		'b_low': ('', '#d64e4e'),
		'b_crit': ('', '#d64e4e'),
		'b_plugged': ('', '#93bbd6'),
		'b_unknown': ('', '#ff4800')
	}

	battery = psutil.sensors_battery()
	if not battery:
		print('{0} N/A\n'.format(output_map['b_unknown'][0]))
		print(output_map['b_unknown'][1])
		sys.exit(0)

	secsleft = battery.secsleft  # by default

	if battery.power_plugged:
		output = output_map['b_plugged']
		secsleft = 0  # irrelevant at this point.
	elif 100 >= battery.percent >= 60:
		output = output_map['b_high']
	elif 59 >= battery.percent >= 16:
		output = output_map['b_mid']
	elif 15 >= battery.percent >= 0:
		output = output_map['b_crit']

	timeleft = datetime.timedelta(seconds=secsleft)

	# icon - percentage - livetime
	fmt = '{0}: - {1:.1f}% - {2}\n'
	out = fmt.format(
		output[0],
		battery.percent,
		timeleft
	)

	print(out)
	print(output[1])


if __name__ == '__main__':
	main()
