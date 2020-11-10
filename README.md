# Command & Control Discord
> Author: Andrew Eng
> Date: 2020-11-10
> Version: 0.1

## Description
This app is a c2 client for command and control over discord.  
Create your discord bots and give it proper accesses.  I dumped my credentials in my home folder under secrets and created a symbolic link within the folder to it.  

Use cases:
1. You want to be able to control your nodes from a discord chat.  Maybe you don't wnat to port forward your connections through your router, or maybe the ISP is blocking it
2. You are a pentester and want an easy encrypted c2 channel to your target
3. You think it's cool, so you cloned it and currently running it.

To issue commands, enter @<botname> cmd <command to execute>.  
You can also DM the bot directly and say "ip" to get the latest ip info for the client.

```python
python3 chat.py
```
