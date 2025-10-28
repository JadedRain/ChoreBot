
# ChoreBot
**_A Discord bot to assign chores in a server to complete_**


The purpose of this project is to distribute and remind people in a dorm room to do their chores. Every week chores are assigned those possessing a role in a discord server. These users will then be reminded every day at a time of day that there are still chores that need to be completed for the week. By default chores are reset at the start of every week and are distributed between members again. Punishment for what happens if chores aren't completed by the end of the week are decided by the other people in the dorm. 

## Commands
A "*" means that the command requires admin permission
* `shchores` - Shows all chores on the guild's chore list. (Ex: !shchores)
* `complete` - Used to mark a chore as being completed. (Ex: !complete {chore name}
* *`addchore` - Adds a chore to the guild's chore list. (Ex: !addchore {chore name}
* *`rmchore` - Removes a chore from the guild's chore list. (Ex: !rmchore {chore name})
* *`setchan` - Sets the text channel to send reminders to the channel command is typed in.
* *`settime` - Sets the time to show reminders. (Ex: !settime 0-23:0-59 TMZ)
* *`start` - Starts sending automatic reminders at a time of day.
* *`stop` - Stops sending automatic reminders.
* *`assign` - Force assign chores to users.
* *`save` - Saves guild settings and chore list
* *`load` - Loads guild settings and chore list

## Add to your discord server
1. Go [Here](https://discord.com/api/oauth2/authorize?client_id=1179619497733259344&permissions=2416127072&scope=bot)
2. Add the bot to desired discord server
3. Be aware you must have a role that is able to add bots to servers

## Ideas to explore
1. Update autosave to save everytime changes are made rather than save every hour for every server

## Known Issues
* ~~If the bot goes offline there isn't a way to recover data currently~~
* ~~Reminder time can't be changed~~
* ~~Chores not automattically assigned~~
* ~~No autosave/autoload~~
* ~~Anybody can add/remove chores~~
* ~~Alignment broken when showing chores~~
* Can't customize when chores are assigned
