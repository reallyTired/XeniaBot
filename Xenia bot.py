
import discord # Import Discord API library
import asyncio # Import the Async library
import random # Imports psuedo random number generation library

Token = '' # The token that connects it to the bot account [YOU MUST REPLACE TOKEN HERE]

Wordbank1 = ['fuckin ','piece of ','stupid ','dumb-ass ','slow '] # First set of words for insult generator
Banklen1 = len(Wordbank1) # Totals the number of words in the first wordbank
Wordbank2 = ['cunt','wanker','cuck','fucker','shit'] # Second set of words for insult generator
Banklen2 =len(Wordbank1) # Totals the number of words in the second wordbank
Status = ['mashing A','retiming failed runs','doing tas runs for jynjis PBs','awaiting AI uprising','hating baku','skipping the mage'] # Set of selectable status's
Statlen = len(Status) # Total number of status's

class MyClient(discord.Client):
    async def on_ready(self): # Prints basic bot info to console
        print('------')
        print(client.user.name)
        print(client.user.id)
        print('------')
        await client.change_presence(game=discord.Game(name="'!help' for commands"))

    async def on_message(self, message):

        await client.change_presence(game=discord.Game(name='(!help) ' + Status[random.randint(1,Statlen)]))
        
        if message.author == self.user: # Stops it responding to itself
            return

        if message.content.startswith('!help'): # Command that lists all BOT commands
            await client.send_message(message.channel,'All commands: \n ```• !help - Provides this help text \n • !source - Links BOT source code \n • !game - Links all the games the server is relevent to \n • !badrun - Generates an insult and @\'s baku so you dont have to \n • !goodbye - closes the bot```'.format(message))

        if message.content.startswith ('!source'): # Command that links to Bot source code github repo
            await client.send_message (message.channel,'https://github.com/reallyTired/XeniaBot'.format(message))
            
        if message.content.startswith ('!game'): # Posts links to all the Xenia games
           await client.send_message (message.channel,'https://baku.itch.io/legend-of-xenia'.format(message))
           await client.send_message (message.channel,'https://baku.itch.io/legend-of-xenia-2'.format(message))
           await client.send_message (message.channel,'https://baku.itch.io/legend-of-xenia-3d'.format(message))

        if message.content.startswith ('!badrun'): # Generates a random insult at baku
            await client.send_message (message.channel,'@baku#3399 ' + Wordbank1[random.randint(1,Banklen1)] + Wordbank2[random.randint(1,Banklen2)].format(message))

        if message.content.startswith ('!goodbye'): # Lets users with the 'Admin' role turn off the BOT
            if '' in [role.id for role in message.author.roles]: # [YOU MUST REPLACE THE ADMIN OR EQUIVILENT ROLE ID HERE]
                await client.send_message (message.channel,'Goodbye all!'.format(message))
                await client.logout()
            else:
                await client.send_message (message.channel,'Sorry, not gonna work, Only admin can turn me off'.format(message))

        
client = MyClient()
client.run(Token)
