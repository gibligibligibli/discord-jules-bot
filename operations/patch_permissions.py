import discord
import core.permissions
from core.permissions import *

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

core.permissions.set_channel_permissions = patched_set_channel_permissions
