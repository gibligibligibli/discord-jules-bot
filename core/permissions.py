import discord

async def set_channel_permissions(session, channel_id, target_id, target_type,
                                   allow=None, deny=None):
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


async def sync_channel_permissions(session, channel_id):
    guild = session.guild
    channel = guild.get_channel(channel_id)
    if not channel:
        session.log("ERRO", f"Canal ID {channel_id} não encontrado")
        return
    await channel.edit(sync_permissions=True, reason="Jules session: sincronizar permissões")
    session.log("OK", f"Permissões de #{channel.name} sincronizadas com a categoria")


async def get_channel_overwrites(session, channel_id):
    guild = session.guild
    channel = guild.get_channel(channel_id)
    if not channel:
        session.log("ERRO", f"Canal ID {channel_id} não encontrado")
        return []

    overwrites = []
    for target, overwrite in channel.overwrites.items():
        allow = [p for p, v in overwrite.pair()[0] if v]
        deny = [p for p, v in overwrite.pair()[1] if v]
        overwrites.append({
            "target_id": target.id,
            "target_name": str(target),
            "target_type": "role" if isinstance(target, discord.Role) else "member",
            "allow": allow,
            "deny": deny,
        })

    session.log("OK", f"{len(overwrites)} permissões especiais em #{channel.name}")
    return overwrites
