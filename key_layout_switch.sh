#!/usr/bin/env bash
# Author: Chris S. https://github.com/nevious
#
# Based on the script of Patrick Haun
#

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

function get_current_layout {
	echo $(setxkbmap -query | awk '
		BEGIN{layout="";variant=""}
		/^layout/{layout=$2}
		/^variant/{variant=" ("$2")"}
		END{printf("%s%s",layout,variant)}'
	)
}

function set_keyboard_layout {
	if [[ ${!#} -eq 1 ]]; then
		setxkbmap ${@:1:$#-1}
		return $?
	fi
}

DEFAULT_LAYOUT="us"
TARGET_LAYOUT=${BLOCK_INSTANCE:-$DEFAULT_LAYOUT}
CURRENT_LAYOUT=$(get_current_layout)

if [[ -n $BLOCK_BUTTON ]]; then
	set_keyboard_layout $TARGET_LAYOUT $BLOCK_BUTTON && CURRENT_LAYOUT=$(get_current_layout)
fi

echo $CURRENT_LAYOUT
