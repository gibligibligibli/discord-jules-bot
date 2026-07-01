import discord
from discord.ext import commands
import json
import os
from datetime import datetime


class SessionBot:
    def __init__(self, guild_id):
        self.guild_id = guild_id
        self.intents = discord.Intents.default()
        self.intents.message_content = True
        self.intents.members = True
        self.bot = commands.Bot(command_prefix="!", intents=self.intents)
        self.guild = None
        self.results = []

    @property
    def on_ready(self):
        return self._on_ready_handler

    @on_ready.setter
    def on_ready(self, handler):
        @self.bot.event
        async def _on_ready():
            self.guild = self.bot.get_guild(self.guild_id)
            if not self.guild:
                self.log("ERRO", f"Servidor {self.guild_id} não encontrado")
                await self.bot.close()
                return
            await handler(self)

    async def run(self, token):
        await self.bot.start(token)

    async def close(self):
        await self.bot.close()

    def log(self, status, details):
        entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "status": status,
            "details": details,
        }
        self.results.append(entry)
        print(f"  [{status}] {details}")

    def save_results(self, path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.results, f, ensure_ascii=False, indent=2)
        print(f"Resultados salvos em: {path}")
