/* 
 *  DISCORD APPLICATION SERVER 
 *  ANIMESH TRIPATHY
 */

TOKEN = "NTA1MjIxNzQ3NDM2NTUyMjMy.DrQcXQ.C_JgPstt1ows_brG48WQ5RLmtG4";

const Discord = require('discord.js');
const client = new Discord.Client();
const helper = require('./helper-functions');

// All commands
const cmdOptions = {
  "help": 0,
  "register": 1,
  "roles": 2,
  "join": 3,
  "leave": 4,
  "report": 3,
  "remove": 4
};

client.on('ready', () => {
  console.log("Pick-Up League of Legends application running...");
});

// Create an event listener for new members
client.on('guildMemberAdd', member => {
  // Send the message to a designated channel on a server
  const channel = member.guild.channels.find(ch => ch.name === 'welcome');
  // Do nothing if the channel wasn't found on this server
  if (!channel) return;
  // Send the message, mentioning the member
  channel.send(`Welcome to the Pick-Up League, ${member}. Make sure to check out #info.`);
});

// Check user commands
client.on('message', async (message) => {
	// Prevent bot from responding to its own messages
    if(message.author == client.user) return;
    // Prevent bot from processing non-commands
    if(message.content.startsWith("!")){
		// Remove the pivot value and parse the command
   		let fullMessage = message.content.substr(1);
    	let tokens = fullMessage.split(" ");
    	let command = tokens[0];
    	// All other words are arguments for the command
    	let args = tokens.slice(1);

    	var returnMessage = "";
    	var discordId = message.author.tag.split("#")[1];
    	switch(cmdOptions[command]){
    		case 0:
    			returnMessage = helper.help();
    			break;
    		case 1:
    			returnMessage = await helper.register(discordId,args);
    			break;
    		case 2:
    			returnMessage = await helper.roles(discordId,args);
    			break;
    		case 3:
    			returnMessage = await helper.join(discordId);
    			break;
    		case 4:
    			returnMessage = await helper.leave(discordId);
    			break;
    		case 5:
    			returnMessage = await helper.report(discordId);
    			break;
    		case 6:
    			returnMessage = await helper.remove(discordId);
    			break;
    		default:
    			returnMessage = "Invalid command. Try running `!help`";
    	}
        message.channel.send(returnMessage);
    }
    //Otherwise we ignore the message
});

// Login to Discord
client.login(TOKEN);


