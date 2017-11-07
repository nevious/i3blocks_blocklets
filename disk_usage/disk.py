#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import subprocess


def get_disk_stats(mp):
	stat = os.statvfs(mp)

	total = stat.f_blocks * stat.f_frsize / 1024 ** 3
	avail = stat.f_bavail * stat.f_frsize / 1024 ** 3
	used = total - avail

	return {
		'avail': avail,
		'total': total,
		'used': used,
		'per_c': 100 * used / total
	}


def launch_ncdu(mp):
	cmd = [
		'/usr/bin/sakura',
		'-t',
		'pop-up',
		'-e',
		'/usr/bin/ncdu %s' % mp,
		'-x',
	]

	subprocess.Popen(
		cmd,
		stdout=open(os.devnull, 'w'),
		stderr=subprocess.STDOUT
	)


def parse_args():
	args = {
		'warn_threshold': 80,
		'crit_threshold': 90,
		'warn_color': '#d6af4e',
		'crit_color': '#d64e4e',
		'format': '{used:.1f}G/{total:.1f}G ({per_c:.1f}%) -  {avail:.1f}G'
	}

	try:
		for arg in sys.argv[1:]:
			key, value = arg.split('=')
			args[key] = int(value) if value.isdigit() else value
	except (KeyError, ValueError):
		# ValuError in case user does something weird
		pass

	return args


def get_instance():
	p = os.getenv('BLOCK_INSTANCE')
	if p and os.path.exists(p):
		return p

	return os.getenv('HOME')


def main():

	output_color = ''
	args = parse_args()
	m_point = get_instance()
	stats = get_disk_stats(m_point)

	# get some more info when not called by i3blocks
	if not os.getenv('BLOCK_NAME'):
		print('Args: %s' % args)
		print('Stats: %s' % stats)
		print('Mount Point: %s' % m_point)

	# print stats with format if given
	print(args['format'].format(**stats))
	print()

	# determine color
	if args['crit_threshold'] > int(stats['per_c']) >= args['warn_threshold']:
		output_color = args['warn_color']
	elif stats['per_c'] >= args['crit_threshold']:
		output_color = args['crit_color']

	print(output_color)

	# handle click-event
	_button = os.getenv('BLOCK_BUTTON')
	if _button and int(_button) == 1:
		launch_ncdu(m_point)


if __name__ == '__main__':
	main()
