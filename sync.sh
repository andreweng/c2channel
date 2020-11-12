#!/bin/bash

# Synch up github
git add -A &&
git commit -m "synched via script" &&
git push &&

echo "Synched from local machine to github."
