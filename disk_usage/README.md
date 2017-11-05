# Customizable disk block for i3blocks

Script checks the disk usage of **$BLOCK_INSTANCE** using pythons **os.statvfs** module. If the instance isn't set the Home-directory of the executing user will be set as default.

So to select a partition configure the instance:

```
[disk_nas]
label=:
instance=/nas
interval=30
command=disk
```

Additionally the script can take more arguments passed to it by command-line in a key=value fashion. The following is supported:

* Warning Threshold (**_warn_threshold=70_**)
* Crititcal Threshold (**_crit_threshold=80_**)
* Warning Color (**_warn_color=#90ce00_**)
* Critical Color (**_crit_color=#ce2500_**)
* Output Format (**_format="{format}"_**)

format is directly used by pythons string formatting.

So in order to achieve the following output:

```
: 119.3G used of 518.5 total beeing 23.0%
```

the following *format*-argument must be passed to the script:

```
format="{used:.1f}G used of {total:.1f} total beeing {per_c}%"
```
Quotes are required for format.

## Example:

```
[disk_root]
label=:
instance=/
interval=30
command=disk format="{used:.1f}G used of {total:.1f} Total beeing {per_c}%" warn_color=#90ce00
```

## Click events

Upon a click event a terminal is opened with ncdu running for the configured partition. To adapt this to your personal setup, you'll need to change the function **launch_ncdu()**:

```python
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
```

Personally, I launch sakura with *pop-up* as title, which i can then use to configure i3 to set the window into floating mode:

```
for_window [title="pop-up"] floating enable border none sticky
```

Output of the launch-command will be redirected to /dev/null

## Dependancies

The script uses only standard python modules and should therefore run on any python environment or should easily be made to run.

## Help

* Advanced String Formatting: https://www.python.org/dev/peps/pep-3101/
