#!/bin/bash
# Create logs
touch chat.log &&
touch command_dm.log &&
touch nohup.out &&
touch command.log && 

# Remove logs
rm chat.log &&
rm command_dm.log &&
rm nohup.out &&
rm command.log &&

# Synch up github
git add -A &&
git commit -m "synched via script" &&
git push &&

echo "Synched from local machine to github."
