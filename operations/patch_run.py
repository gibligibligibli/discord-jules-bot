import sys
import discord
from discord.ext import commands
import core.client
import logging
import bot

logging.basicConfig(level=logging.INFO)

def new_init(self, guild_id):
    self.guild_id = guild_id
    self.intents = discord.Intents.default()
    self.intents.message_content = False
    self.intents.members = False
    self.bot = commands.Bot(command_prefix="!", intents=self.intents)
    self.guild = None
    self.results = []

def new_setter(self, handler):
    @self.bot.event
    async def on_ready():
        self.guild = self.bot.get_guild(int(self.guild_id))
        if not self.guild:
            self.log("ERRO", f"Servidor {self.guild_id} não encontrado")
            await self.bot.close()
            return
        await handler(self)

core.client.SessionBot.__init__ = new_init
core.client.SessionBot.on_ready = property(lambda self: None, new_setter)

import core.permissions
async def patched_set_channel_permissions(session, channel_id, target_id, target_type, allow=None, deny=None):
    guild = session.guild
    channel = guild.get_channel(channel_id)
    if not channel:
        session.log("ERRO", f"Canal ID {channel_id} não encontrado")
        return

    if target_type == "role":
        target = guild.get_role(target_id)
    else:
        target = guild.get_member(target_id)

    if not target:
        session.log("ERRO", f"{target_type} ID {target_id} não encontrado")
        return

    kwargs = {}
    if allow:
        for p in allow: kwargs[p] = True
    if deny:
        for p in deny: kwargs[p] = False

    overwrite = discord.PermissionOverwrite(**kwargs)
    await channel.set_permissions(target, overwrite=overwrite, reason="Jules session: definir permissões (PATCHED)")

    alvo_nome = target.name if hasattr(target, "name") else str(target)
    session.log("OK", f"Permissões de #{channel.name} para {alvo_nome} atualizadas")

bot.ACTION_MAP["set_channel_permissions"] = patched_set_channel_permissions


import operations.patch_channels
bot.ACTION_MAP['create_channel'] = operations.patch_channels.patched_create

import operations.patch_send
bot.main()
