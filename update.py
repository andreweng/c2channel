import os

chat_pid = os.system("ps aux | grep 'chat' | grep -v grep | awk -F '  ' '{print $2}'")
kill_chat = 'kill -9 ' + str(chat_pid)
git_update = 'git pull https://github.com/andreweng/c2channel.git'

os.system(git_update)
os.system(kill_chat)
