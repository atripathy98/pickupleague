/* 
 *  HELPER FUNCTIONS
 *  ANIMESH TRIPATHY
 */
const fbconn = require('./firebase-connector');
const riotapi = require('./riot-api');

// Import JSON files
const mmrData = require('./resources/mmr.json');
const allRoles = {
    "TOP": 0,
    "JGL": 1,
    "MID": 2,
    "ADC": 3,
    "SUP": 4,
};

// Register command
exports.help = function(){
    return "COMING SOON!";
};

// Register command
exports.register = async function(discordId,args){
    if(args.length == 0)
        return "Invalid format. Try using: `!register <Summoner Name>`";
    var summonerName = args.join('').toLowerCase().replace(/\s/g,'');
    // Check if user is already registered
    var existingPlayer = await fbconn.getSummoner(summonerName,"unformattedName");
    // && (currentDate.getTime() - existingPlayer.time) < 86400000*2
    if(existingPlayer.success)
        return "Summoner name has already been registered.";
    // Attempt to register user
    var summonerData = await riotapi.getSummoner(summonerName);
    if(!summonerData.success)
        return "Error: Unable to find summoner <VALUE>";

    // Incoming Summoner to service
    var accountData = {};
    accountData.unformattedName = summonerName;
    accountData.summonerName = summonerData.data.name;
    accountData.id = summonerData.data.id.toString();
    accountData.accountId = summonerData.data.accountId.toString();
    accountData.summonerLevel = summonerData.data.summonerLevel;
    accountData.lastUpdated = (new Date()).getTime();
    accountData.discordId = discordId;
    
    // Gather Ranked Info
    var hiddenInfo = {};
    hiddenInfo["LADDER"] = {};
    hiddenInfo["LADDER"]["wins"] = 0;
    hiddenInfo["LADDER"]["losses"] = 0;
    hiddenInfo["LADDER"]["mmr"] = 1200;
    hiddenInfo["LADDER"]["autofill"] = 0;
    hiddenInfo["LADDER"]["totalGames"] = 0;
    var rankedJSON = await riotapi.getRankedData(accountData.id);
    if(rankedJSON.success){
        var rankedData = rankedJSON.data;
        rankedData.forEach(function(value){
            if(value.queueType === "RANKED_FLEX_SR" || value.queueType === "RANKED_SOLO_5x5"){
                hiddenInfo[value.queueType] = {};
                hiddenInfo[value.queueType]["tier"] = value.tier;
                hiddenInfo[value.queueType]["rank"] = value.rank;
                hiddenInfo[value.queueType]["wins"] = value.wins;
                hiddenInfo[value.queueType]["losses"] = value.losses;
                hiddenInfo[value.queueType]["mmr"] = mmrData[value.tier][value.rank] + Math.round(60.0*(value.leaguePoints/100.0));
            }
        });
    }
    fbconn.insertAccountData(accountData);
    return "Registration successful! Use `!roles` to set roles.";
};

// Roles command
exports.roles = async function(discordId,args){
    if(args.length < 2)
        return "Invalid format. Try using: `!roles <Main Role> <Secondary Role>`";
    // Confirm summoner exists first
    var existingPlayer = await fbconn.getSummoner(discordId,"discordId");
    if(!existingPlayer.success)
        return "Invalid request. Use `!register` first to join service!";
    var mainRole = args[0].toUpperCase();
    var secondaryRole = args[1].toUpperCase();
    if(!allRoles.hasOwnProperty(mainRole) || !allRoles.hasOwnProperty(secondaryRole))
        return "Invalid roles. Confirm that roles are of the following: TOP, JGL, MID, ADC, SUP.";
    fbconn.setRoles(existingPlayer.id,allRoles[mainRole],allRoles[secondaryRole]);
    return "Roles successfully set! Use `!join` to enter queue.";
};

// Join command
exports.join = async function(discordId){
    // Confirm summoner exists first
    var existingPlayer = await fbconn.getSummoner(discordId,"discordId");
    if(!existingPlayer.success)
        return "Invalid request. Use `!register` first to join service!";
    if(!existingPlayer.userReady)
        return "Invalid request. Use `!roles` first to join queue.";

    var inQueuePlayer = await fbconn.checkQueue(discordId);
    if(inQueuePlayer.success){
        return "Already in queue! Please be more patient.";
    }
    fbconn.addSummonerToQueue(existingPlayer.id,discordId);
    return "Successfully joined queue. Waiting for more players...";
};

// Leave command
exports.leave = async function(discordId){
    // Confirm summoner exists first
    var inQueuePlayer = await fbconn.checkQueue(discordId);
    if(!inQueuePlayer.success)
        return "Invalid request. Cannot leave without first joining.";
    fbconn.leaveQueue(inQueuePlayer.key);
    return "Successfully left queue.";
};

// Report command
exports.report = async function(discordId){
    return "Under implementation! Please check back soon.";
};

// Remove command
exports.remove = async function(discordId){
    return "Under implementation! Please check back soon.";
};


