#!/bin/zsh
open $(sed "$1!d" ~/ZoomCron/links.txt)
~/ZoomCron/venv/bin/python3 ~/ZoomCron/talk_to_server.py $1
