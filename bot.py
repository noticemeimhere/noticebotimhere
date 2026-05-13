from dotenv import load_dotenv
from datetime import datetime
import os
from twitchAPI.twitch import Twitch
from twitchAPI.oauth import UserAuthenticator
from twitchAPI.type import AuthScope, ChatEvent
from twitchAPI.chat import Chat, EventData, ChatMessage, ChatSub, ChatCommand
import asyncio

load_dotenv()



SECRET_ID = os.getenv('SECRET_ID')
SECRET_PASS = os.getenv('SECRET_PASS')
USER_SCOPE = [AuthScope.CHAT_READ, AuthScope.CHAT_EDIT]
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

async def test(cmd: ChatCommand):
    await cmd.reply(f'pong')

async def helpcmd(cmd: ChatCommand):
    await cmd.reply(f"Commands: !ping, !time, !whatdoing")

async def time(cmd: ChatCommand):
    await cmd.reply(f"The local time is: {datetime.now().strftime("%H:%M:%S")}")

async def whatdoing(cmd: ChatCommand):
    await cmd.reply(whatdoingvar)

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
        auth = UserAuthenticator(twitch,USER_SCOPE)
        token, refresh_token = await auth.authenticate()
        with open(TOKEN_FILE, "w") as f:
            f.write(refresh_token)

    chat = await Chat(twitch)
    chat.register_event(ChatEvent.READY, on_ready)
    chat.register_event(ChatEvent.MESSAGE, on_message)



    chat.register_command('ping', test)
    chat.register_command('help', helpcmd)
    chat.register_command('time', time)
    chat.register_command('whatdoing', whatdoing)
    chat.register_command('setdoing', setdoing)



    chat.start()
    try:
        input('press ENTER to stop\n')
    finally:
        chat.stop()
        await twitch.close()


asyncio.run(run())