# noticebotimhere
Thanks to the pytwitchAPI developers for making this work.
This is the bot I use for my twitch streams. It can respond to simple commands and give you some information based on how its setup.

## Requirements
This requires a .env file in the same directory as the python file, inside you need:
```
SECRET_ID=your_client_id
SECRET_PASS=your_secret_key
```
These can be obtained after creating an application at the [Twitch developer dashboard](https://dev.twitch.tv/console/apps/create).
You will also need the dotenv and twitchAPI packages.
Set the redirect url in your Twitch application to ```http://localhost:17563```

## Usage

Run the ```bot.py``` file, if you see ```.ENV FILE MISSING OR NOT READ``` in the console then make sure your variables in the .env file are properly named.
A Twitch authentication page will open in your default brower, make sure you are logged into your bot's account, then click authorize.
If everything works, a confirmation page should open, and the bot will print into the console, ```I am alive, is nice.```. There should be a new file in your directory called token.txt, this will allow you to skip the authorization from now on. The bot should now be running, how amazing.

