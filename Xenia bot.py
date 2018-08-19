import discord # Import Discord API library
import asyncio # Import the Async library
import random # Imports psuedo random number generation library
import re # Imports pattern stuff

prefixes = ['+', '!', 'n!']

admins = ['Admin', 'VAC B&']

pattern = re.compile("[^\s\"']+|\"([^\"]*)\"|'([^']*)'") # Sets up a regexp for later

Token = 'NDgwMDU2MDE5OTg5NDMwMjc0.DliyyA.MEsH1Ce9ECMJMdt4nOjW_XYjOWo' # The token that connects it to the bot account 

class MyClient(discord.Client):
    async def on_ready(self): # Prints basic bot info to console
        print('------')
        print(client.user.name)
        print(client.user.id)
        print('------')
        await client.change_presence(game=discord.Game(name="'!help' for commands"))
        
    async def on_message(self, message):

        if message.author == self.user: # Stops it responding to itself
            return
        
        raw = message.content
        
        data = [i.group(0) for i in re.finditer(pattern, raw) if any([raw.startswith(i) for i in prefixes])]
        
        if not data:
            return
        
        command = {'command': data[0].lstrip("".join(prefixes)), 'args': data[1:]}
        
        try:
            call = getattr(MyClient, command['command'])
            await call(message, *command['args'])
        
        except Exception as e:
            print(e)
            await client.send_message(message.channel, '\'{}\' is not a command.'.format(command['command']))
            return

    async def help(message, *args): # Command that lists all BOT commands
        await client.send_message(message.channel, 'All commands: \n``` • !help - Provides this help text \n • !source - Links BOT source code \n • !game - Links all the games the server is relevent to \n • !goodbye - closes the bot``` ')

    async def source(message, *args): # Command that links to Bot source code github repo
        await client.send_message(message.channel, 'https://github.com/reallyTired/XeniaBot')
        
    async def game(message, *args): # Posts links to all the Xenia games
        await client.send_message(message.channel, 'https://baku.itch.io/legend-of-xenia\nhttps://baku.itch.io/legend-of-xenia-2\nhttps://baku.itch.io/legend-of-xenia-3d')

    async def wr(message, *args): # posts Any% WR for desired game
        if args[0] == 'lox1':
            await client.send_message(message.channel, 'LoX1 wr not implemented yet')
            
        elif args[0] == 'lox2':
            await client.send_message(message.channel, 'LoX2 wr not implemented yet')
            
        else:
            await client.send_message(message.channel, args[0] + ' wr not implemented yet')

    async def goodbye(message, *args): # Lets users with the 'Admin' role turn off the BOT
        if set([role.name for role in message.author.roles if role.name != '@everyone']).issubset(set(admins)) and len(message.author.roles) > 1:
            await client.send_message(message.channel, 'Goodbye all!')
            await client.logout()
        else:
            await client.send_message(message.channel, 'Sorry, not gonna work, only admins can turn me off')
            
client = MyClient()
client.run(Token)