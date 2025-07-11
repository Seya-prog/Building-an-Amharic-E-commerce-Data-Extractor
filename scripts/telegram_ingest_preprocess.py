"""telegram_ingest_preprocess.py
================================
Task 1: Data Ingestion & Pre-processing for EthioMart E-commerce NER project.

This script connects to Telegram, downloads messages from a list of Ethiopian
Telegram e-commerce channels, performs light Amharic-aware text normalisation,
and saves both the raw and pre-processed messages to the `data/` directory.

Requirements
------------
1. Environment variables providing Telegram API credentials:
   - TG_API_ID – numeric API ID from https://my.telegram.org
   - TG_API_HASH – corresponding API hash string
   Optionally you can set TG_SESSION_NAME to use an alternate Telethon
   session file name (defaults to "ecommerce_scraper").

2. A list of target channel usernames in the CHANNELS list below.

Running
-------
$ pip install -r requirements.txt
$ python scripts/telegram_ingest_preprocess.py

Two CSV files will be produced in the `data/raw` and `data/preprocessed`
sub-folders, suffixed with the current timestamp.
"""

from __future__ import annotations

import asyncio
import os
import re
from datetime import datetime
from pathlib import Path
from typing import List

import csv
from telethon import TelegramClient
from telethon.tl.types import Message
from dotenv import load_dotenv

# ---------------------------------------------------------------------------
# Configuration – edit as required -----------------------------------------
# ---------------------------------------------------------------------------
load_dotenv('.env')
API_ID = int(os.getenv('TG_API_ID'))
API_HASH = os.getenv('TG_API_HASH')
SESSION_NAME = 'ecommerce_scraper'

# Active Ethiopian e-commerce Telegram channels
CHANNELS: List[str] = [
    "@Shewabrand",
    "@helloomarketethiopia",
    "@gebeyaadama",
    "@ZemenExpress",
    "@ethio_brand_collection",
    "@AwasMart",
    "@qnashcom",
]

# Limit per channel (set higher for more data; mind Telegram rate limits)
LIMIT_PER_CHANNEL: int = 3000

RAW_DATA_DIR = Path("data/raw")
PREPROCESSED_DIR = Path("data/preprocessed")
MEDIA_DIR = Path("data/media")  # Store downloaded images/documents

RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
PREPROCESSED_DIR.mkdir(parents=True, exist_ok=True)
MEDIA_DIR.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------------------
# Helper functions ----------------------------------------------------------
# ---------------------------------------------------------------------------

def clean_amharic_text(text: str) -> str:
    """Light normalisation for Amharic text.

    1. Removes line-breaks.
    2. Collapses multiple spaces.
    3. Keeps Amharic punctuation marks (።፥፣፤፦፧፡፠) and word characters.
    4. Strips leading/trailing whitespace.
    """
    # Handle None values
    if text is None:
        return ""
        
    # Remove control characters / newlines
    text = re.sub(r"[\r\n]+", " ", text)
    # Remove everything except word chars, spaces and common Amharic punctuation
    text = re.sub(r"[^\w\s።፥፣፤፦፧፡፠]", "", text, flags=re.UNICODE)
    # Collapse whitespace
    text = re.sub(r"\s+", " ", text)
    return text.strip()


async def scrape_channel(client: TelegramClient, channel_username: str, writer, media_dir: str) -> None:
    """Scrape data from a single channel and write to CSV."""
    entity = await client.get_entity(channel_username)
    channel_title = entity.title if entity.title else channel_username
    async for message in client.iter_messages(entity, limit=LIMIT_PER_CHANNEL):
        media_path = None
        if message.media and hasattr(message.media, 'photo'):
            # Create a unique filename for the photo
            filename = f"{channel_username}_{message.id}.jpg"
            media_path = os.path.join(media_dir, filename)
            # Download the media to the specified directory if it's a photo
            await client.download_media(message.media, media_path)
        
        # Write the channel title along with other data
        writer.writerow([
            channel_title,
            f"https://t.me/{channel_username}",
            message.id,
            message.message or "",
            message.date.isoformat() if message.date else None,
            media_path
        ])


async def main() -> None:
    if API_ID is None or API_HASH is None:
        raise RuntimeError(
            "TG_API_ID and TG_API_HASH must be set as environment variables. "
            "Obtain them from https://my.telegram.org and export before running."
        )

    client = TelegramClient(SESSION_NAME, API_ID, API_HASH)
    
    # Create a directory for media files
    media_dir = 'photos'
    os.makedirs(media_dir, exist_ok=True)

    # Open the CSV file and prepare the writer
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_path = RAW_DATA_DIR / f"telegram_data_{timestamp}.csv"
    
    async with client:
        await client.start()
        
        with open(csv_path, 'w', newline='', encoding='utf-8-sig') as file:
            writer = csv.writer(file)
            writer.writerow([
                'Channel Title',
                'Channel Username',
                'Message ID',
                'Message',
                'Date',
                'Media Path'
            ])
            
            # Scrape each channel
            for channel in CHANNELS:
                print(f"Scraping data from {channel}...")
                try:
                    await scrape_channel(client, channel, writer, media_dir)
                    print(f"  → Successfully scraped {channel}")
                except Exception as exc:
                    print(f"  ! Failed to scrape {channel}: {exc}")

    print(f"\nAll data has been saved to: {csv_path.relative_to(Path.cwd())}")


if __name__ == "__main__":
    asyncio.run(main())
