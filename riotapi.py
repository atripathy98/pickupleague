# CUSTOM RIOT API FRAMEWORK
# Author: Animesh Tripathy <a.tripathy101@gmail.com>
# Created: October 25, 2018
# Updated: October 26, 2018
# Purpose: Efficiently utilize Riot API to retrieve data

# Import URL Library
import json
from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.parse import quote

base_api_key = "RGAPI-ca99041e-f455-4571-be1c-4d6e5c8d24a7"
tourney_api_key = "RGAPI-d6725b47-cbd7-40d0-a565-570e64c0f93c"
base_url = "https://na1.api.riotgames.com/lol"
methods = ["/summoner/v3/summoners/by-name/", "/league/v3/positions/by-summoner/"]

# Main query format to request Riot API
def get_data_from_riot(full_url):
	response = {}
	response["success"] = True
	try:
		request = urlopen(full_url)
	except HTTPError as err:
		# NEED TO HANDLE 429 and 404
		if err.code == 404:
			response["success"] = False
		else:
			raise
	if response["success"]:
		encoding = request.info().get_content_charset('utf8')
		data = json.loads(request.read().decode(encoding))
		response["data"] = data
	return response

# Get Summoner data based on Summoner name
def get_player_data_by_summoner(summoner):
	full_url = base_url + methods[0] + summoner + "?api_key=" + base_api_key
	return get_data_from_riot(full_url)

def get_ranked_data_by_summoner(summoner_id):
	full_url = base_url + methods[1] + summoner_id + "?api_key=" + base_api_key
	return get_data_from_riot(full_url)



# 	//GENERATE TOURNAMENT CODES x(number)
# exports.getTourneyCode = async function(number){
#   var headArr = {
#     "mapType": "SUMMONERS_RIFT",
#     "metadata": "",
#     "pickType": "TOURNAMENT_DRAFT",
#     "spectatorType": "ALL",
#     "teamSize": 5
#   };
#   const options = {
#     json: true,
#     method:"POST",
#     url: "https://americas.api.riotgames.com/lol/tournament/v3/codes?count="+number.toString()+"&tournamentId=302545&api_key="+tourneyapi,
#     body: headArr
#   };
#   return await getDataFromRiotGames(options);
# }