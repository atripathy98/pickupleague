# ---------------------------
#  DISCORD APPLICATION SERVER 
#  ANIMESH TRIPATHY
# ---------------------------
import discord
#from discord.ext import commands

TOKEN = "NTA1MjIxNzQ3NDM2NTUyMjMy.DrQcXQ.C_JgPstt1ows_brG48WQ5RLmtG4"

client = discord.Client()

#bot = commands.Bot(command_prefix='$')

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    if message.content.startswith('!hello'):
        msg = 'Hello {0.author.mention}'.format(message)
        await client.send_message(message.channel, msg)

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN)