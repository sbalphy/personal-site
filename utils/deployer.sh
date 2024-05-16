#!/bin/bash
# made this a separate utility so I can run it from Windows
python rssupdater.py

# deploy files to server via rsync
rsync -Cav --exclude={'utils','README.txt'} -e "ssh -p 14641" ../ sunny@fleming.cecm.usp.br:public_html