const admin = require('firebase-admin');

//FIREBASE PRIVATE SERVICE KEY
const serviceAccount = require('./resources/serviceAccountKey.json');
admin.initializeApp({
  credential: admin.credential.cert(serviceAccount),
  databaseURL: "https://risingsummoners-e4e70.firebaseio.com"
});

//FIREBASE DB
const db = admin.database();
const queueRef = db.ref("/queue");
const summonerRef = db.ref("/summoners");


// Get summoner info by searching for searchTerm within searchChild key
exports.getSummoner = async function(searchTerm,searchChild){
	var response = {};
	try{
    	const snapshot = await summonerRef.orderByChild(searchChild).equalTo(searchTerm).once('value');
    	if(snapshot.numChildren() != 0){
    		response.success = true;
			var datum = snapshot.val();
			var key = Object.keys(datum)[0];
			response.time = datum[key]["lastUpdated"];
			response.id = datum[key]["id"];
			response.userReady = (datum[key].hasOwnProperty("mainRole") && datum[key].hasOwnProperty("secRole"));
		}else{
			response.success = false;
		}
    }catch(err){
    	response.success = false;
    	response.status = err.status;
    }
	return response;
}

// Get summoner info by searching for searchTerm within searchChild key
exports.checkQueue = async function(discordId){
	const snapshot = await queueRef.orderByChild("discordId").equalTo(discordId).once('value');
	var response = {
		success: false
	};
    if(snapshot.numChildren() != 0){
		response.success = true;
		response.key = Object.keys(snapshot.val())[0];
	}
	return response;
}

exports.insertAccountData = function(accountData){
	var updateData = {};
	updateData[accountData.id] = accountData;
	summonerRef.update(updateData);
}

exports.addSummonerToQueue = function(id,discordId){
	var playerRef = queueRef.push();
	playerRef.set({
		id: id,
		discordId: discordId,
		key: playerRef.key
	});
	return true;
}

exports.leaveQueue = function(key){
	var playerRef = queueRef.child("/"+key)
	playerRef.remove();
}

exports.setRoles = function(id,main,secondary){
	var rolesRef = summonerRef.child(id);
	rolesRef.update({
		mainRole: main,
		secRole: secondary
	});
}