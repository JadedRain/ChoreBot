
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


## Skills Demonstrated:
These skills are located inside at: https://github.com/JadedRain/ChoreBot/blob/master/ChoreBot/commands/chore_commands.py#L250
- Object-Oriented
- Decorators
- Exception handling
- Dictionaries

### Object-Oriented
I wrapped the commands inside of an object in order to benefit from inheriting from a class from the library I'm using to make calls with my discord bot.

### Decorators
Taking advantage of a decorator from this library in order to listen for commands from users inside of a server

### Exception handling
Lines: 78-86
Here I have exception handling to make sure that the user was inputing the correct format for the command

### Dictionaries
Here I use a dictionary to keep track of what guilds are using my application in order to update them whenever a change needs to be made. I made the choice to store them inside of the bot rather than a database as when this application was originally made, I didn't have the skills to work with a database

## Known Issues
* ~~If the bot goes offline there isn't a way to recover data currently~~
* ~~Reminder time can't be changed~~
* ~~Chores not automattically assigned~~
* ~~No autosave/autoload~~
* ~~Anybody can add/remove chores~~
* ~~Alignment broken when showing chores~~
* Can't customize when chores are assigned
