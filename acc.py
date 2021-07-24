
from telethon import TelegramClient, client
import asyncio
from telethon.tl.functions.account import UpdateProfileRequest
from pywinauto.application import Application
from telethon.tl.functions.channels import JoinChannelRequest,LeaveChannelRequest
api_id = 7840210
api_hash = "3c2fad223fb0d6a3ee39a798ce7a1ec3"
phone_number = "+84971763672"
# bot =  TelegramClient(phone_number, api_id, api_hash).start(phone=phone_number, max_attempts=10)
client = TelegramClient(phone_number, api_id, api_hash)
async def run():
    result = await client.start(phone=phone_number)
    print(result)
with client:
    run()
    print("Successfully started")
    print("Open your telegram client")
    client.run_until_disconnected()