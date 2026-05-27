from dotenv import load_dotenv
from datetime import datetime
import os
import random
from twitchAPI.twitch import Twitch
from twitchAPI.oauth import UserAuthenticator
from twitchAPI.type import AuthScope, ChatEvent
from twitchAPI.chat import Chat, EventData, ChatMessage, ChatSub, ChatCommand
from twitchAPI.helper import first
import asyncio

load_dotenv()



SECRET_ID = os.getenv('SECRET_ID')
SECRET_PASS = os.getenv('SECRET_PASS')
USER_SCOPE = [AuthScope.CHAT_READ, AuthScope.CHAT_EDIT, AuthScope.MODERATOR_READ_FOLLOWERS]
CHANNEL = 'noticemeimhere'
TOKEN_FILE = "token.txt"

if(SECRET_ID == None or SECRET_PASS == None):
    print(".ENV FILE MISSING OR NOT READ")
    quit()

whatdoingvar = "@noticemeimhere, SETUP PLEASE!!!!!"

async def on_ready(ready_event: EventData):
    print('I am alive, is nice.')
    await ready_event.chat.join_room(CHANNEL)

async def on_message(msg: ChatMessage):
    print(f'{msg.user.name}: {msg.text}')

# Commands

async def ping(cmd: ChatCommand):
    await cmd.reply(f'pong')

async def commands(cmd: ChatCommand):
    await cmd.reply(f"Commands: !time, !what, !discord, !roll (number), !followtime")

async def gettime(cmd: ChatCommand):
    await cmd.reply(f"The local time is {datetime.now().strftime("%I:%M%p")}")

async def what(cmd: ChatCommand):
    await cmd.reply(whatdoingvar)
    cmd.user

async def discord(cmd: ChatCommand):
    await cmd.reply("Join the server! discord.gg/fHxHjgFDWD")

async def dice(cmd: ChatCommand):
    if(cmd.parameter.isdigit()):
        try:
            a = int(cmd.parameter)
            if(a <= 1000):
                await cmd.reply(f"Rolling a {cmd.parameter} sided die...")
                await asyncio.sleep(1)
                await cmd.reply(f"You rolled a {random.randint(1, int(cmd.parameter))}.")
            else:
                await cmd.reply("Please roll a number less than or equal to 1000.")
        except ValueError:
            await cmd.reply("Input not valid")
        
    else:
        #space before cmd.parameter ensures that any input starting with "/" is not confused as a chat command by twitch, if there is no space bot will not reply
        await cmd.reply(f" {cmd.parameter} is not a whole number.")

async def followtime(cmd: ChatCommand):
    target = await first(cmd.chat.twitch.get_users(logins=cmd.user.name))
    steamer = await first(cmd.chat.twitch.get_users(logins=CHANNEL))

    follower = await first(await cmd.chat.twitch.get_channel_followers(broadcaster_id=steamer.id, user_id=target.id))

    if follower:
        timefollowed = datetime.now(follower.followed_at.tzinfo) - follower.followed_at
        days = timefollowed.days
        await cmd.reply(f"{target.display_name} has been following for {days} days since {follower.followed_at.strftime('%b %d, %Y')}!")
    else:
        await cmd.reply(f"{target.display_name} is not following {CHANNEL} ):.")

# moderator only commands
async def setdoing(cmd: ChatCommand):
    global whatdoingvar
    if(cmd.user.mod):
        whatdoingvar = cmd.parameter
        await cmd.reply(f"Set whatdoing to {cmd.parameter}!")
    elif(cmd.user.name == "noticemeimhere"):
        whatdoingvar = cmd.parameter
        await cmd.reply(f"Set whatdoing to {cmd.parameter}!")
    else:
        await cmd.reply(f"You do not have permissions to use this command!")

# doesnt work due to permission issues but maybe ill implement if i feel like it
# async def settitle(cmd:ChatCommand):
#     if(cmd.user.mod or cmd.user.name == "noticemeimhere"):  
#         streamer = await first(cmd.chat.twitch.get_users(logins=CHANNEL))
#         await cmd.chat.twitch.modify_channel_information(broadcaster_id=streamer.id, title=cmd.parameter)
#         await cmd.reply("got here")
#     else:
#         await cmd.reply(f"You do not have permission to use this command.")

#main
async def run():
    twitch = await Twitch(SECRET_ID, SECRET_PASS)

    if os.path.exists(TOKEN_FILE):
        print("Token found!")
        with open(TOKEN_FILE, "r") as f:
            refresh_token = f.read()
        await twitch.set_user_authentication(None,USER_SCOPE,refresh_token)

    else:
        print("No token found")
        auth = UserAuthenticator(twitch, USER_SCOPE)
        token, refresh_token = await auth.authenticate()
        await twitch.set_user_authentication(token, USER_SCOPE, refresh_token)
        with open(TOKEN_FILE, "w") as f:
            print("Writing token to token.txt...")
            f.write(refresh_token)

    chat = await Chat(twitch)
    chat.register_event(ChatEvent.READY, on_ready)
    chat.register_event(ChatEvent.MESSAGE, on_message)



    chat.register_command('ping', ping)
    chat.register_command('help', commands)
    chat.register_command('cmds', commands)
    chat.register_command('commands', commands)
    chat.register_command('time', gettime)
    chat.register_command('what', what)
    chat.register_command('setdoing', setdoing)
    chat.register_command('discord', discord)
    chat.register_command("roll", dice)
    chat.register_command("followtime", followtime)

    chat.start()
    try:
        input('press ENTER to stop\n')
    finally:
        chat.stop()
        await twitch.close()


asyncio.run(run())