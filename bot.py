# ---------------------------
#  DISCORD APPLICATION SERVER 
#  ANIMESH TRIPATHY
# ---------------------------
import asyncio
import discord
import lolpickup as pick

TOKEN = "NTA1MjIxNzQ3NDM2NTUyMjMy.DrQcXQ.C_JgPstt1ows_brG48WQ5RLmtG4"

#bot = commands.Bot(description="LoL Pick-Up Games Bot by animesh#8975", command_prefix='.', pm_help = False)
client = discord.Client()

# ------------------------------------------------------
# EVENT LISTENER: on_message(message)
# Parse message for incoming commands from users
# ------------------------------------------------------

@client.async_event
def on_message(message):
    # Prevent bot from responding to its own messages
    if message.author == client.user:
        return

    # Prevent bot from processing non-commands
    if message.content[0] != '!':
        return

    # Parse content for command + arguments
    params = message.content.split(" ")
    command = params[0][1:]
    args = params[1:]

    # Process request made by user and reply accordingly
    response = pick.process_command(message.author.id, command, args)
    yield from client.send_message(message.channel, response)

# On bot start: Log info to console screen
@client.async_event
def on_ready():
    print('Running LoL Pick-Up Bot v1.0.0')
    print('Created by animesh#8975')

client.run(TOKEN)
