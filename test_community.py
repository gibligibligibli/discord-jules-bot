import asyncio
import discord
import os

token = os.environ.get("DISCORD_TOKEN")
guild_id = 1521821316087287808

class Bot(discord.Client):
    async def on_ready(self):
        guild = self.get_guild(guild_id)

        # Check if the HTTP client has a route for it
        try:
            # We can use guild.edit directly, but discord.py might not support features
            features = guild.features.copy()
            if "COMMUNITY" not in features:
                features.append("COMMUNITY")

            payload = {
                "features": features,
                "verification_level": 1,
                "explicit_content_filter": 2,
                "rules_channel_id": 1521859731482742904, # regras
                "public_updates_channel_id": 1521859734704099450 # chat-geral
            }
            await self.http.request(discord.http.Route("PATCH", f"/guilds/{guild.id}"), json=payload)
            print("Community enabled via HTTP request!")
        except Exception as e:
            print("Failed to enable community:", e)

        await self.close()

intents = discord.Intents.default()
intents.message_content = False
intents.members = False
intents.presences = False
client = Bot(intents=intents)
client.run(token)
