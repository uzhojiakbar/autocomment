import os
import random
import asyncio
from telethon import TelegramClient, events
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
from telethon.errors import FloodWaitError

# Telegram API sozlamalari
api_id = '13035049'
api_hash = '1f08e6980689fa2e2d558f16a0d7bdcc'
phone = '+998956466040'
client = TelegramClient('account', api_id, api_hash)

with open('k.txt', 'r') as file:
    channels = [int(line.strip().replace('-100', '')) for line in file.readlines()]

with open('ch.txt', 'r') as file:
    kanal = [int(line.strip().replace('-100', '')) for line in file.readlines()]


with open('texts.txt', 'r') as file:
    comments = [line.strip() for line in file.readlines()]

async def main():
    await client.start(phone)
    
    # Mavjud kanallar ro'yxatini olish
    dialogs = await client(GetDialogsRequest(
        offset_date=None,
        offset_id=0,
        offset_peer=InputPeerEmpty(),
        limit=200,
        hash=0
    ))

    # Tekshirish uchun dialogs ma'lumotlarini chop etish
    print("Dialogs: ", dialogs)

    # Kanallarni filtrlash
    # channel_ids = [dialog.id for dialog in dialogs.chats if hasattr(dialog, 'username') and dialog.username in channels]
    # kanal_id = [dialog.id for dialog in dialogs.chats if hasattr(dialog, 'username') and dialog.username in kanal]
    # channel_ids = [channels]
    # kanal_id = [kanal]

    
    # Filtrlangan kanallarni chop etish
    print("Filtrlangan kanallar: ", kanal)

    @client.on(events.NewMessage(chats=channels))
    async def handler(event):
        try:
            # Forward qilingan xabarlarni tekshirish
            print("YANGI HABAR")
            if event.message.fwd_from and event.message.fwd_from.from_id.channel_id in kanal :
                print(event.message.fwd_from.from_id.channel_id in kanal)
                print("ID", event.message.fwd_from.from_id.channel_id)
                print("Forward qilingan kanal xabari aniqlandi.")
                comment = random.choice(comments)
                try:
                    await client.send_message(event.message.to_id, comment, reply_to=event.message.id)
                    print(f"Sharh qo'shildi: {comment}")
                except FloodWaitError as e:
                    print(f"FloodWaitError: {e}. Kutish va qayta urinish.")
                    await asyncio.sleep(e.seconds)
                    await client.send_message(event.message.to_id, comment, reply_to=event.message.id)
                    print(f"Sharh qo'shildi: {comment} (Qayta urinishdan keyin)")
            else:
                print("Forward qilingan xabar yoki kanal ID mos kelmadi.")
        except Exception as e:
            print(f"Xato: {e}")

    print("Bot ishga tushdi...")
    await client.run_until_disconnected()

with client:
    client.loop.run_until_complete(main())


# MessageFwdHeader(
#      from_id=PeerChannel(channel_id=2214802039), from_name=None, channel_post=30, post_author=None, saved_from_peer=PeerChannel(channel_id=2214802039), saved_from_msg_id=30, saved_from_id=None, saved_from_name=None, saved_date=None, psa_type=None)

