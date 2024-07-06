import os
import random
import discord
import asyncio
from googleapiclient.discovery import build
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')
CHANNEL_ID = int(os.getenv('CHANNEL_ID'))

client = discord.Client()

youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

async def fetch_random_video():
    request = youtube.search().list(
        part='snippet',
        q='blugray',
        maxResults=50,  # Augmenter le nombre de résultats pour plus de diversité
        order='date',
        type=''  # Rechercher tous les types de contenu
    )
    response = request.execute()
    if response['items']:
        random_item = random.choice(response['items'])
        return f"https://www.youtube.com/watch?v={random_item['id']['videoId']}"
    return None

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    channel = client.get_channel(CHANNEL_ID)
    while True:
        random_video_url = await fetch_random_video()
        if random_video_url:
            await channel.send(random_video_url)
        await asyncio.sleep(60)  # Attendre 1 minute

client.run(DISCORD_TOKEN)
