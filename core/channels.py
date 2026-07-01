import discord

async def create(session, nome, tipo="text", categoria=None, topico=None):
    guild = session.guild
    tipo_map = {"text": discord.ChannelType.text, "voice": discord.ChannelType.voice,
                 "forum": discord.ChannelType.forum, "announcement": discord.ChannelType.news}
    channel_type = tipo_map.get(tipo, discord.ChannelType.text)

    category_obj = None
    if categoria:
        category_obj = discord.utils.get(guild.categories, name=categoria)

    reason = f"Jules session: criar canal #{nome}"
    if channel_type in (discord.ChannelType.voice,):
        novo = await guild.create_voice_channel(nome, category=category_obj, reason=reason)
    elif channel_type == discord.ChannelType.forum:
        novo = await guild.create_forum(nome, topic=topico, category=category_obj, reason=reason)
    else:
        novo = await guild.create_text_channel(nome, topic=topico, category=category_obj, reason=reason)

    session.log("OK", f"Canal #{novo.name} ({tipo}) criado (ID: {novo.id})")
    return novo


async def edit(session, channel_id, nome=None, topico=None, categoria=None, posicao=None, nsfw=None, slowmode_delay=None):
    guild = session.guild
    channel = guild.get_channel(channel_id) or await guild.fetch_channel(channel_id)

    kwargs = {}
    if nome is not None:
        kwargs["name"] = nome
    if topico is not None:
        kwargs["topic"] = topico
    if categoria is not None:
        kwargs["category"] = discord.utils.get(guild.categories, name=categoria)
    if posicao is not None:
        kwargs["position"] = posicao
    if nsfw is not None:
        kwargs["nsfw"] = nsfw
    if slowmode_delay is not None:
        kwargs["slowmode_delay"] = slowmode_delay

    if kwargs:
        await channel.edit(**kwargs, reason="Jules session: editar canal")

    session.log("OK", f"Canal #{channel.name} editado ({', '.join(kwargs.keys())})")
    return channel


async def delete(session, channel_id):
    guild = session.guild
    channel = guild.get_channel(channel_id) or await guild.fetch_channel(channel_id)
    nome = channel.name
    await channel.delete(reason="Jules session: deletar canal")
    session.log("OK", f"Canal #{nome} deletado")


async def list_channels(session):
    guild = session.guild
    canais = []
    for ch in guild.channels:
        canais.append({
            "id": ch.id,
            "name": ch.name,
            "type": str(ch.type).split(".")[-1],
            "category": ch.category.name if ch.category else None,
            "position": ch.position,
        })
    session.log("OK", f"{len(canais)} canais listados")
    return canais
