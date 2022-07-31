#!/usr/bin/env bash
SHELL=/bin/bash
DISPLAY=:0
PATH=$PATH:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin
cd /home/selmi/socialMediaAutomation/lnpybot
echo '' > run/likes.log
py lnpybot/cli.py --env --headless --username LINKEDIN_EMAIL_ADDRESS --password LINKEDIN_PASSWORD --follow-network