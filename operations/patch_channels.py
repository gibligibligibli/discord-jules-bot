import discord
import core.channels
from core.channels import *

async def patched_create(session, nome, tipo="text", categoria=None, topico=None):
    guild = session.guild
    tipo_map = {"text": discord.ChannelType.text, "voice": discord.ChannelType.voice,
                 "forum": discord.ChannelType.forum, "announcement": discord.ChannelType.news,
                 "category": discord.ChannelType.category}
    channel_type = tipo_map.get(tipo, discord.ChannelType.text)

    category_obj = None
    if categoria:
        category_obj = discord.utils.get(guild.categories, name=categoria)

    reason = f"Jules session: criar canal/categoria #{nome}"
    if channel_type == discord.ChannelType.category:
        novo = await guild.create_category(nome, reason=reason)
    elif channel_type in (discord.ChannelType.voice,):
        novo = await guild.create_voice_channel(nome, category=category_obj, reason=reason)
    elif channel_type == discord.ChannelType.forum:
        novo = await guild.create_forum(nome, topic=topico, category=category_obj, reason=reason)
    else:
        novo = await guild.create_text_channel(nome, topic=topico, category=category_obj, reason=reason)

    session.log("OK", f"Canal #{novo.name} ({tipo}) criado (ID: {novo.id})")
    return novo

core.channels.create = patched_create
