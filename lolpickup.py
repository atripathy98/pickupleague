# LoL PICK-UP LEAGUE BOT FRAMEWORK
# Author: Animesh Tripathy <a.tripathy101@gmail.com>
# Created: October 25, 2018
# Updated: October 26, 2018
# Purpose: Module to utilize pick-up league application

# Import Async IO
import asyncio
import json
import firebasehelper as fbconn
import riotapi
import time

# Roles list
all_roles = {"TOP": 0, "JGL": 1, "MID": 2, "ADC": 3, "SUP": 4}

# Open MMR json file
with open('./resources/mmr.json') as f:
	mmr_data = json.load(f)

# ------------------------------------------------------
# HELP COMMAND
# RETURN TYPE: STRING
# Returns list of commands with specified details
# ------------------------------------------------------
def help():
	return "HELP: Under implementation! Please check back soon."

# ------------------------------------------------------
# REGISTER COMMAND
# PARAMETERS: (Discord ID, Arguments)
# RETURN TYPE: STRING
# Returns information regarding registration attempt
# ------------------------------------------------------
def register(userid, args):
	# Check if summoner name is provided
	if len(args) == 0:
		return "Invalid format. Try using: `!register <Summoner Name>`"

	# Check if user is already registered
	existing_player = fbconn.find_within("/summoners",userid,"discordId")
	if existing_player["success"]:
		return "Discord account already connected to an account."

	# Gather data on new summoner
	summoner = ("".join(args)).lower().replace(" ","")
	player_info = riotapi.get_player_data_by_summoner(summoner)
	if not player_info["success"]:
		return "Error: Unable to find summoner: "+summoner

	# Format player data
	player_data = player_info["data"]
	account_data = {}
	account_data["unformattedName"] = summoner
	account_data["summonerName"] = player_data["name"]
	account_data["id"] = str(player_data["id"])
	account_data["accountId"] = str(player_data["accountId"])
	account_data["summonerLevel"] = player_data["summonerLevel"]
	account_data["lastUpdated"] = int(time.time())
	account_data["discordId"] = userid

	# Establish hidden ranked data
	hidden_info = {}
	hidden_info["LADDER"] = {}
	hidden_info["LADDER"]["wins"] = 0
	hidden_info["LADDER"]["losses"] = 0
	hidden_info["LADDER"]["mmr"] = 1200
	hidden_info["LADDER"]["autofill"] = 0
	hidden_info["LADDER"]["totalGames"] = 0

	# Collect ranked data for player if any
	ranked_info = riotapi.get_ranked_data_by_summoner(account_data["id"])
	if ranked_info["success"]:
		ranked_data = ranked_info["data"][0]
		for queue in ranked_data:
			datum = ranked_data[queue]
			# Only process queue if either solo or flex
			if queue != "RANKED_FLEX_SR" or queue != "RANKED_SOLO_5x5":
				continue
			hidden_info[queue] = {}
			hidden_info[queue]["tier"] = datum["tier"]
			hidden_info[queue]["rank"] = datum["rank"]
			hidden_info[queue]["wins"] = datum["wins"]
			hidden_info[queue]["losses"] = datum["losses"]
			hidden_info[queue]["mmr"] = mmr_data[datum["tier"]][datum["rank"]] + round(60.0*(datum["leaguePoints"]/100.0))

	# Insert new user into database
	account_data["mmrData"] = hidden_info
	fbconn.insert_data("/summoners",account_data)
	return "Registration successful! Use `!choose <Main Role> <Secondary>` to set your roles."

# ------------------------------------------------------
# CHOOSE COMMAND
# PARAMETERS: (Discord ID, Arguments)
# RETURN TYPE: STRING
# Returns information regarding choose attempt
# ------------------------------------------------------
def choose(userid, args):
	# Check if summoner name is provided
	if len(args) < 2:
		return "Invalid format. Try using: `!choose <Main Role> <Secondary>`"

	# Confirm summoner exists first
	existing_player = fbconn.find_within("/summoners",userid,"discordId")
	if not existing_player["success"]:
		return "Invalid request. Use `!register <Summoner Name>` first before picking roles!"

	# Check if roles are valid
	main_role = args[0].upper()
	secondary_role = args[1].upper()
	if main_role not in all_roles or secondary_role not in all_roles:
		return "Invalid roles. Confirm that roles are of the following: TOP, JGL, MID, ADC, SUP."

	# Update database with roles
	datum = {"mainRole": all_roles[main_role], "secRole": all_roles[secondary_role]}
	fbconn.update_data("/summoners", existing_player["key"], datum)
	return "Roles successfully set! Use `!join` to enter queue."

# ------------------------------------------------------
# JOIN COMMAND
# PARAMETERS: (Discord ID)
# RETURN TYPE: STRING
# Returns information regarding join attempt
# ------------------------------------------------------
def join(userid):
	# Confirm summoner exists
	existing_player = fbconn.find_within("/summoners",userid,"discordId")
	if not existing_player["success"]:
		return "Invalid request. Use `!register <Summoner Name>` first before joining queue!"

	# Confirm summoner has picked roles
	if not fbconn.roles_chosen(existing_player["key"]):
		return "Invalid request. Use `!choose <Main Role> <Secondary>` first before joining queue!"

	# Confirm existing player is not already in queue
	in_queue = fbconn.find_within("/queue",userid,"discordId")
	if in_queue["success"]:
		return "Already in queue! Please be more patient."

	# Insert userid into queue
	fbconn.insert_data("/queue",{"discordId": userid})
	return "Successfully joined queue. Waiting for more players..."

# ------------------------------------------------------
# LEAVE COMMAND
# PARAMETERS: (Discord ID)
# RETURN TYPE: STRING
# Returns information regarding leave attempt
# ------------------------------------------------------
def leave(userid):
	# Confirm summoner exists
	existing_player = fbconn.find_within("/summoners",userid,"discordId")
	if not existing_player["success"]:
		return "Invalid request. Use `!register <Summoner Name>` before using that command."

	# Confirm existing player is not already in queue
	in_queue = fbconn.find_within("/queue",userid,"discordId")
	if not in_queue["success"]:
		return "Invalid request. Cannot leave queue without first joining."

	# Remove userid from queue
	fbconn.delete_data("/queue",in_queue["key"])
	return "Successfully left queue."

# ------------------------------------------------------
# REMOVE COMMAND
# PARAMETERS: (Discord ID)
# RETURN TYPE: STRING
# Returns information regarding remove attempt
# ------------------------------------------------------
def remove(userid):
	# Confirm summoner exists
	existing_player = fbconn.find_within("/summoners",userid,"discordId")
	if not existing_player["success"]:
		return "Invalid request. Use `!register <Summoner Name>` before using that command."

	# Confirm existing player is not already in queue
	in_queue = fbconn.find_within("/queue",userid,"discordId")
	if in_queue["success"]:
		leave(userid)

	# Remove userid from queue
	fbconn.delete_data("/summoners",existing_player["key"])
	return "Successfully removed. Sorry to see you go :("

# ------------------------------------------------------
# INVALID COMMAND
# RETURN TYPE: STRING
# Returns only when no commands are recognized
# ------------------------------------------------------
def invalid():
	return "Invalid command. Try running `!help`"

# ------------------------------------------------------
# PROCESS COMMAND
# RETURN TYPE: STRING
# Returns useful information on command execution
# ------------------------------------------------------
def process_command(userid, command, args):
	# Process incoming command
	if command == "help":
		return help()
	elif command == "register":
		return register(userid,args)
	elif command == "choose":
		return choose(userid,args)
	elif command == "join":
		return join(userid)
	elif command == "leave":
		return leave(userid)
	elif command == "remove":
		return remove(userid)
	else:
		return invalid()
