from dotenv import load_dotenv
import os
from twitchAPI.twitch import Twitch
from twitchAPI.oauth import UserAuthenticator
from twitchAPI.type import AuthScope, ChatEvent
from twitchAPI.chat import Chat, EventData, ChatMessage, ChatSub, ChatCommand
import asyncio

load_dotenv()

SECRET_ID = os.getenv('SECRET_ID')
SECRET_PASS = os.getenv('SECRET_PASS')

print(SECRET_ID)
print(SECRET_PASS)