// RIOT API CALLS
const request = require('request-promise');

// RIOT API KEYS
const baseapi = "RGAPI-ca99041e-f455-4571-be1c-4d6e5c8d24a7";
const tourneyapi = "RGAPI-d6725b47-cbd7-40d0-a565-570e64c0f93c";

async function getDataFromRiotGames(options){
  var response = {};
  try{
    response.data = await request(options);
    response.success = true;
  }catch(err){
    response.success = false;
    response.error = err.statusCode;
    response.message = "Requested data was not found or Riot API reached rate limit.";
  }
  return response;
}

//GET SUMMONER DATA
exports.getSummoner = async function(summonerName){
	const options = {
    method:'GET',
    json: true,
    url: encodeURI("https://na1.api.riotgames.com/lol/summoner/v3/summoners/by-name/"+summonerName+"?api_key="+baseapi)
  };
  return await getDataFromRiotGames(options);
}

exports.getRankedData = async function(summonerid){
	const options = {
    method:'GET',
    json: true,
    url: "https://na1.api.riotgames.com/lol/league/v3/positions/by-summoner/"+summonerid+"?api_key="+baseapi
  };
  return await getDataFromRiotGames(options);
}