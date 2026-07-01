import discord
from discord.ext import commands
import json
import os
from datetime import datetime

class SessionBot:
    def __init__(self, guild_id):
        self.guild_id = int(guild_id)
        self.intents = discord.Intents.default()
        # Disable privileged intents so it works without intent approval
        self.intents.message_content = False
        self.intents.members = False
        self.intents.presences = False
        self.bot = commands.Bot(command_prefix="!", intents=self.intents)
        self.guild = None
        self.results = []
        self.log_channel_id = None

    @property
    def on_ready(self):
        return self._on_ready_handler

    @on_ready.setter
    def on_ready(self, handler):
        self._on_ready_handler = handler
        @self.bot.event
        async def on_ready():
            self.guild = self.bot.get_guild(self.guild_id)
            if not self.guild:
                self.log("ERRO", f"Servidor {self.guild_id} não encontrado")
                await self.bot.close()
                return

            # Find log and result channel IDs
            for ch in self.guild.channels:
                if "logs-jules" in ch.name.lower():
                    self.log_channel_id = ch.id
                if "resultados-jules" in ch.name.lower():
                    self.results_channel_id = ch.id

            await handler(self)

    async def send_log_realtime(self, status, details, message_ref=None):
        if self.log_channel_id and self.guild:
            ch = self.guild.get_channel(self.log_channel_id)
            if ch:
                if status == "EM ANDAMENTO":
                    emoji = "ℹ️"
                elif status == "OK":
                    emoji = "✅"
                elif status in ("ERRO", "FALHA"):
                    emoji = "❌"
                else:
                    emoji = "ℹ️"

                content = f"[{emoji} {status}] {details}"
                try:
                    if message_ref:
                        await message_ref.edit(content=content)
                        return message_ref
                    else:
                        return await ch.send(content)
                except Exception as e:
                    print(f"Erro ao enviar/editar log em tempo real: {e}")
        return None

    async def send_result_message(self, content):
        if hasattr(self, 'results_channel_id') and self.results_channel_id and self.guild:
            ch = self.guild.get_channel(self.results_channel_id)
            if ch:
                try:
                    await ch.send(content)
                except Exception as e:
                    print(f"Erro ao enviar resultado final: {e}")

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
