import os
import random
import time
import asyncio
from telethon import TelegramClient, events
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
from telethon.errors import FloodWaitError

# Telegram API sozlamalari
api_id = '13035049'
api_hash = '1f08e6980689fa2e2d558f16a0d7bdcc'
phone = '+998956466040'
client = TelegramClient('nomer4274', api_id, api_hash)

with open('k.txt', 'r') as file:
    channels = [int(line.strip().replace('-100', '')) for line in file.readlines()]

with open('ch.txt', 'r') as file:
    kanal = [int(line.strip().replace('-100', '')) for line in file.readlines()]


with open('texts.txt', 'r') as file:
    comments = [line.strip() for line in file.readlines()]

# Maqsadli ID
target_id = 6915875567
karta = "**TONKEEPER: UQDpP6_B71wddbX_fKQhIvgUOK3sfIn91Aebxa66Q3mR-ZVv\n\nUZCARD: 8600120423085573**"
yozdikmi = 0


async def main():
    await client.start(phone)
    
    print("Filtrlangan kanallar: ", kanal)

    @client.on(events.NewMessage(chats=channels))
    async def handler(event):
        global yozdikmi
        try:
            # Forward qilingan xabarlarni tekshirish
            print("YANGI HABAR")
            
            if event.message.fwd_from and event.message.fwd_from.from_id.channel_id in kanal and yozdikmi==0:
                print("Forward qilingan kanal xabari aniqlandi.")
                comment = random.choice(comments)
                try:
                    await client.send_message(event.message.to_id, comment, reply_to=event.message.id)
                    yozdikmi+=1
                    print(f"Sharh qo'shildi: {comment}")
                except FloodWaitError as e:
                    print(f"FloodWaitError: {e}. Kutish va qayta urinish.")
                    await asyncio.sleep(e.seconds)
                    await client.send_message(event.message.to_id, comment, reply_to=event.message.id)
                    print(f"Sharh qo'shildi: {comment} (Qayta urinishdan keyin)")

            # Reply kelgan xabarni tekshirish
            if event.message.sender_id == target_id and yozdikmi:
                time.sleep(5)
                print(f"Reply keldi ID: {target_id}")
                await event.reply(karta or "@cardmine")
                yozdikmi = 0
                print("salom test yuborildi.")
            else:
                print("Forward qilingan xabar yoki kanal ID mos kelmadi.")
        except Exception as e:
            print(f"Xato: {e}")

    print("Bot ishga tushdi...")
    await client.run_until_disconnected()

with client:
    client.loop.run_until_complete(main())
