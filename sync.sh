#!/bin/bash
# Remove databases
rm chat.log &&
rm command.log &&
rm nohup.out &&

# Synch up github
git add -A &&
git commit -m "synched via script" &&
git push &&

echo "Synched from local machine to github."
