from telethon import TelegramClient
import csv
import asyncio
import os
from datetime import datetime
from telethon.errors import FloodWaitError

# Your API credentials
api_id = '23132032'
api_hash = '4d79f9a3231fc4eef4111efa450a9d66'

# List of channels to scrape
channels = [
    '@ZemenExpress',
    '@nevacomputer',
    '@ethio_brand_collection',
    '@Leyueqa',
    '@Shageronlinestore'
]

# Directory and filename for data
data_dir = r'C:\Users\ayedr\amharic-ecommerce-ner\data\raw'
os.makedirs(data_dir, exist_ok=True)
file_path = os.path.join(data_dir, 'all_messages.csv')

# Number of messages to fetch per channel
TARGET_MESSAGES_PER_CHANNEL = 100000

def load_existing_ids():
    existing_ids = set()
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader, None)  # skip header
            for row in reader:
                if len(row) >= 2:
                    existing_ids.add(row[1])  # message ID
    return existing_ids
async def fetch_channel_messages(client, channel_name, existing_ids):
    try:
        entity = await client.get_entity(channel_name)
    except Exception as e:
        print(f"Failed to get entity for {channel_name}: {e}")
        return
    
    message_count = 0
    last_message_id = None
    while True:
        try:
            # Fetch messages in batches of 1000
            if last_message_id is None:
                messages = await client.get_messages(entity, limit=1000)
            else:
                messages = await client.get_messages(entity, limit=1000, max_id=last_message_id)
            if not messages:
                break  # No more messages
            for message in messages:
                if message.id in existing_ids:
                    continue
                if message_count >= TARGET_MESSAGES_PER_CHANNEL:
                    break
                # Save message details
                with open(file_path, 'a', encoding='utf-8', newline='') as f:
                    writer = csv.writer(f)
                    if os.path.getsize(file_path) == 0:
                        writer.writerow(['timestamp', 'sender_id', 'message_text', 'views', 'channel'])
                    writer.writerow([
                        message.date.strftime('%Y-%m-%d %H:%M:%S') if message.date else '',
                        message.sender_id,
                        message.message,
                        getattr(message, 'views', ''),
                        channel_name
                    ])
                existing_ids.add(message.id)
                message_count += 1
            last_message_id = messages[-1].id
            # Respect rate limits
            await asyncio.sleep(1)
        except FloodWaitError as e:
            print(f"Rate limit hit: sleeping for {e.seconds} seconds")
            await asyncio.sleep(e.seconds)
        except Exception as e:
            print(f"Error fetching messages from {channel_name}: {e}")
            break
    print(f"Fetched {message_count} messages from {channel_name}")
async def main():
    existing_ids = load_existing_ids()
    client = TelegramClient('session_name', api_id, api_hash)
    await client.start()

    for channel in channels:
        print(f"Starting to fetch messages from {channel}")
        await fetch_channel_messages(client, channel, existing_ids)

    await client.disconnect()

if __name__ == '__main__':
    asyncio.run(main())