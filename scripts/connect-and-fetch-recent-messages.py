from telethon import TelegramClient
import csv
import asyncio
import os
from datetime import datetime

# Your API credentials
api_id = '23132032'
api_hash = '4d79f9a3231fc4eef4111efa450a9d66'

# List of channels to scrape
channels = [
    '@ZemenExpress',
    '@meneshayeofficial',
    '@ethio_brand_collection',
    '@Fashiontera',
    '@modernshoppingcenter'
]

# Directory to save data
data_dir = r'C:\Users\ayedr\amharic-ecommerce-ner\data\raw'

# Max messages per file
MAX_MESSAGES_PER_FILE = 1000

# Load existing message IDs from previous files
def load_existing_ids():
    existing_ids = set()
    for filename in os.listdir(data_dir):
        if filename.startswith('messages_') and filename.endswith('.csv'):
            filepath = os.path.join(data_dir, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                for row in reader:
                    if len(row) >= 2:
                        existing_ids.add(row[1])  # message ID
    return existing_ids

# Generate filename based on date and message count
def get_filename(date_str, file_index):
    return os.path.join(data_dir, f'messages_{date_str}_part{file_index}.csv')

async def main():
    client = TelegramClient('session_name', api_id, api_hash)
    await client.start()

    existing_ids = load_existing_ids()

    date_str = datetime.now().strftime('%Y%m%d')
    file_index = 1
    message_count = 0
    filename = get_filename(date_str, file_index)

    # Open first CSV file
    f = open(filename, 'a', encoding='utf-8', newline='')
    writer = csv.writer(f)

    # Write header if file is new
    if os.path.getsize(filename) == 0:
        writer.writerow(['timestamp', 'sender_id', 'message_text', 'views', 'channel'])

    for channel in channels:
        print(f"Fetching messages from {channel}")
        try:
            entity = await client.get_entity(channel)
            async for message in client.iter_messages(entity, limit=100):
                if str(message.id) in existing_ids:
                    continue
                # Rotate file if message count exceeds limit
                if message_count >= MAX_MESSAGES_PER_FILE:
                    f.close()
                    file_index += 1
                    filename = get_filename(date_str, file_index)
                    f = open(filename, 'a', encoding='utf-8', newline='')
                    writer = csv.writer(f)
                    # Write header for new file
                    writer.writerow(['timestamp', 'sender_id', 'message_text', 'views', 'channel'])
                    message_count = 0

                # Save message details
                writer.writerow([
                    message.date.strftime('%Y-%m-%d %H:%M:%S') if message.date else '',
                    message.sender_id,
                    message.message,
                    getattr(message, 'views', ''),
                    channel
                ])
                existing_ids.add(str(message.id))
                message_count += 1
        except Exception as e:
            print(f"Error fetching {channel}: {e}")

    f.close()
    await client.disconnect()

if __name__ == '__main__':
    asyncio.run(main())