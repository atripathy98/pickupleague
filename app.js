/* 
 *  DISCORD APPLICATION SERVER 
 *  ANIMESH TRIPATHY
 */

BOT_TOKEN = "NTA1MjIxNzQ3NDM2NTUyMjMy.DrQcXQ.C_JgPstt1ows_brG48WQ5RLmtG4";

const Discord = require('discord.js');
const client = new Discord.Client();

client.on('ready', () => {
  console.log(`Logged in as ${client.user.tag}!`);
});

// ping -> pong
client.on('message', msg => {
  if (msg.content === 'ping') {
    msg.reply('pong');
  }
});

// Login to Discord
client.login(BOT_TOKEN);

// app.set('port', (process.env.PORT || 5000));
// app.use(express.static(__dirname + '/views'));


