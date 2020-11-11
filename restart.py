import os
import time

pid = os.system("ps aux | grep 'chat' | grep -v grep | awk -F '  ' '{print $2}'")
print(f'Restarting chat service on {pid}')
cmd = 'kill -9 ' + str(pid)
print(f'{cmd}\n is being executed...')
os.system(cmd)

time.sleep(10)

pid = os.system("ps aux | grep 'chat' | grep -v grep | awk -F '  ' '{print $2}'")
print(f'Watchtower restarted the service with a new PID: {pid}')
