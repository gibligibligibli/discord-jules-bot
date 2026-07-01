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

    allow_perms = discord.Permissions()
    deny_perms = discord.Permissions()
    if allow:
        for perm in allow:
            setattr(allow_perms, perm, True)
    if deny:
        for perm in deny:
            setattr(deny_perms, perm, True)

    await channel.set_permissions(target, overwrite=discord.PermissionOverwrite(
        **{p: None for p in dir(discord.Permissions) if not p.startswith("_")}
    ), reason="Jules session: limpar permissões primeiro")

    await channel.set_permissions(
        target,
        overwrite=discord.PermissionOverwrite(
            **{p: None for p in ["send_messages", "read_messages", "manage_messages",
                                  "view_channel", "connect", "speak", "add_reactions",
                                  "attach_files", "embed_links", "use_external_emoji",
                                  "use_external_stickers", "mention_everyone",
                                  "manage_webhooks", "create_instant_invite"]
               if p not in (allow or []) + (deny or [])},
            **{p: True for p in (allow or [])},
            **{p: False for p in (deny or [])},
        ),
        reason="Jules session: definir permissões",
    )

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
