#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import subprocess

def get_disk_stats(mp):
	stat = os.statvfs(mp)

	total = stat.f_blocks * stat.f_frsize/1024**3
	avail = stat.f_bavail * stat.f_frsize/1024**3

	return {
		'avail': avail,
		'total': total,
		'used': total - avail,
		'per_c': 100-(100*avail / total)
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

def main():
	_p = os.getenv('BLOCK_INSTANCE')
	output_color = ''
	warn_color = '#d6af4e'
	crit_color = '#d64e4e'
	warning = 80
	critical = 90
	mount_p = _p if _p else os.getenv('HOME')

	stats = get_disk_stats(mount_p)
	print('%.1fG/%.1fG (%.1f%%)\n' % (
			stats['avail'],
			stats['total'],
			stats['per_c']
		)
	)

	if critical > int(stats['per_c']) >= warning:
		output_color = warn_color
	elif stats['per_c'] >= critical:
		output_color = crit_color

	print(output_color)

	_button = os.getenv('BLOCK_BUTTON')
	if _button and int(_button) == 1:
		launch_ncdu(mount_p)


if __name__ == '__main__':
	main()
