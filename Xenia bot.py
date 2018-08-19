#!/usr/bin/env python

import discord # Import Discord API library
import asyncio # Import the Async library
import random # Imports psuedo random number generation library
import re # Imports pattern stuff

try:
    import srcomapi, srcomapi.datatypes as src
except:
    print("Please run 'pip install srcomapi' to use this bot")

api = srcomapi.SpeedrunCom()

games = api.search(srcomapi.datatypes.Game, {"name": "legend of xenia"})

game_ids = []

for i in games:
    game_ids.append([j for j in i.categories])

if len(game_ids) < 1:
    raise Exception ("Could not connect to API")

prefixes = ['+', '!', 'n!']

admins = ['Admin', 'VAC B&']

pattern = re.compile("[^\s\"']+|\"([^\"]*)\"|'([^']*)'") # Sets up a regexp for later

Token = '' # The token that connects it to the bot account 

try:
    f = open("token.tkn").read()
    Token = f
except Exception as e:
    raise Exception (str(e) + ": please provide a valid Discord token in the token.tkn file!")

def formatTime(time):
    return str(int(time // 60)), str(int(time % 60)).zfill(2), str(time % 1).lstrip("0.")[:3]

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
            if args[1] == "any%":
                time = game_ids[0][0].records[0].runs[0]["run"].times["primary_t"]
                await client.send_message(message.channel, "WR for LoX1 any%: {}:{}.{:<03}".format(*formatTime(time)))
                
            elif args[1] == "100%":
                print("100% selected")
                time = game_ids[0][1].records[0].runs[0]["run"].times["primary_t"]
                await client.send_message(message.channel, "WR for LoX1 100%: {}:{}.{:<03}".format(*formatTime(time)))
            
            else:
                print("invalid choice")
                await client.send_message(message.channel, "{} is not a category for LoX1".format(args[1]))
                
        elif args[0] == 'lox2':
            if args[1] == "any%":
                time = game_ids[1][0].records[0].runs[0]["run"].times["primary_t"]
                await client.send_message(message.channel, "WR for LoX2 any%: {}:{}.{:<03}".format(*formatTime(time)))  
                
            else:
                await client.send_message(message.channel, "{} is not a category for LoX2".format(args[1]))            
            
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