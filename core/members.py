import discord
from datetime import timedelta


async def timeout(session, user_id, minutos, motivo=None):
    guild = session.guild
    member = guild.get_member(user_id)
    if not member:
        session.log("ERRO", f"Membro ID {user_id} não encontrado no servidor")
        return
    duracao = timedelta(minutes=minutos)
    await member.timeout(duracao, reason=motivo or "Jules session: timeout")
    session.log("OK", f"{member} silenciado por {minutos} min ({motivo})")


async def remove_timeout(session, user_id):
    guild = session.guild
    member = guild.get_member(user_id)
    if not member:
        session.log("ERRO", f"Membro ID {user_id} não encontrado")
        return
    await member.timeout(None, reason="Jules session: remover timeout")
    session.log("OK", f"Timeout removido de {member}")


async def kick(session, user_id, motivo=None):
    guild = session.guild
    member = guild.get_member(user_id)
    if not member:
        session.log("ERRO", f"Membro ID {user_id} não encontrado")
        return
    await member.kick(reason=motivo or "Jules session: kick")
    session.log("OK", f"{member} expulso ({motivo})")


async def ban(session, user_id, motivo=None, dias_excluir_mensagens=0):
    guild = session.guild
    member = guild.get_member(user_id)
    if member:
        await member.ban(reason=motivo or "Jules session: ban", delete_message_days=dias_excluir_mensagens)
        session.log("OK", f"{member} banido ({motivo})")
    else:
        await guild.ban(discord.Object(id=user_id), reason=motivo or "Jules session: ban")
        session.log("OK", f"Usuário ID {user_id} banido ({motivo})")


async def get_messages(session, channel_id, user_id=None, limite=100):
    guild = session.guild
    channel = guild.get_channel(channel_id)
    if not channel:
        session.log("ERRO", f"Canal ID {channel_id} não encontrado")
        return []

    mensagens = []
    async for msg in channel.history(limit=limite):
        if user_id and msg.author.id != user_id:
            continue
        mensagens.append({
            "id": msg.id,
            "author": str(msg.author),
            "author_id": msg.author.id,
            "content": msg.content[:500],
            "timestamp": msg.created_at.isoformat(),
            "attachments": [a.url for a in msg.attachments],
        })

    session.log("OK", f"{len(mensagens)} mensagens obtidas de #{channel.name}")
    return mensagens


async def list_members(session, cargo_id=None):
    guild = session.guild
    membros = []
    for m in guild.members:
        if cargo_id and not discord.utils.get(m.roles, id=cargo_id):
            continue
        top_role = m.top_role.name if m.top_role else "Nenhum"
        membros.append({
            "id": m.id,
            "name": str(m),
            "display_name": m.display_name,
            "bot": m.bot,
            "joined_at": m.joined_at.isoformat() if m.joined_at else None,
            "top_role": top_role,
            "roles": [r.name for r in m.roles if not r.is_default()],
        })
    session.log("OK", f"{len(membros)} membros listados")
    return membros
