/* 
 *  DISCORD APPLICATION SERVER 
 *  ANIMESH TRIPATHY
 */

TOKEN = "NTA1MjIxNzQ3NDM2NTUyMjMy.DrQcXQ.C_JgPstt1ows_brG48WQ5RLmtG4";

const Discord = require('discord.js');
const client = new Discord.Client();

client.on('ready', () => {
  console.log("Pick-Up League of Legends application running...");
});

// Create an event listener for new members
client.on('guildMemberAdd', member => {
  // Send the message to a designated channel on a server:
  const channel = member.guild.channels.find(ch => ch.name === 'welcome');
  // Do nothing if the channel wasn't found on this server
  if (!channel) return;
  // Send the message, mentioning the member
  channel.send(`Welcome to the Pick-Up League, ${member}. Make sure to check out #info.`);
});

// Login to Discord
client.login(TOKEN);

// app.set('port', (process.env.PORT || 5000));
// app.use(express.static(__dirname + '/views'));


