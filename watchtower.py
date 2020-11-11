import os, time, logging

cmd = "ps aux | grep 'chat.py' | grep -v grep"

while True: 
    retcode = os.system(cmd)
    if retcode:
        os.system('nohup /usr/bin/python3 ~/c2channel/chat.py &')
        logging.warn('...Disconnected from c2 channel\n Restarting chat.py')
    time.sleep(10)
