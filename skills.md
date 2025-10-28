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
