import discord


async def guild_info(session):
    g = session.guild
    info = {
        "id": g.id,
        "name": g.name,
        "description": g.description,
        "owner": str(g.owner),
        "owner_id": g.owner_id,
        "member_count": g.member_count,
        "online_count": sum(1 for m in g.members if m.status != discord.Status.offline),
        "channel_count": len(g.channels),
        "text_channels": len(g.text_channels),
        "voice_channels": len(g.voice_channels),
        "categories": len(g.categories),
        "role_count": len(g.roles),
        "emoji_count": len(g.emojis),
        "boost_tier": g.premium_tier,
        "boost_count": g.premium_subscription_count,
        "verification_level": str(g.verification_level).split(".")[-1],
        "explicit_content_filter": str(g.explicit_content_filter).split(".")[-1],
        "mfa_level": "required" if g.mfa_level else "not required",
        "nsfw_level": str(g.nsfw_level).split(".")[-1],
        "afk_channel": str(g.afk_channel) if g.afk_channel else None,
        "afk_timeout": g.afk_timeout,
        "system_channel": str(g.system_channel) if g.system_channel else None,
        "rules_channel": str(g.rules_channel) if g.rules_channel else None,
        "created_at": g.created_at.isoformat(),
        "is_large": g.large,
    }
    session.log("OK", f"Informações do servidor '{g.name}' obtidas ({g.member_count} membros)")
    return info


async def channel_info(session, channel_id):
    guild = session.guild
    ch = guild.get_channel(channel_id) or guild.get_thread(channel_id)
    if not ch:
        try:
            ch = await guild.fetch_channel(channel_id)
        except discord.NotFound:
            session.log("ERRO", f"Canal ID {channel_id} não encontrado")
            return None

    info = {
        "id": ch.id,
        "name": ch.name,
        "type": str(ch.type).split(".")[-1],
        "category": ch.category.name if ch.category else None,
        "position": ch.position,
        "topic": getattr(ch, "topic", None),
        "nsfw": getattr(ch, "nsfw", None),
        "slowmode_delay": getattr(ch, "slowmode_delay", 0),
        "created_at": ch.created_at.isoformat(),
        "permissions_synced": getattr(ch, "permissions_synced", None),
        "member_count": len(getattr(ch, "members", [])),
        "is_news": ch.is_news() if hasattr(ch, "is_news") else False,
    }
    session.log("OK", f"Informações do canal #{ch.name} ({info['type']}) obtidas")
    return info


async def role_info(session, role_id):
    guild = session.guild
    r = guild.get_role(role_id)
    if not r:
        session.log("ERRO", f"Cargo ID {role_id} não encontrado")
        return None

    perms_ativas = [p for p, v in dict(r.permissions) if v]
    info = {
        "id": r.id,
        "name": r.name,
        "color": str(r.color),
        "position": r.position,
        "hoist": r.hoist,
        "mentionable": r.mentionable,
        "member_count": len(r.members),
        "is_default": r.is_default(),
        "is_bot_managed": r.is_bot_managed(),
        "is_premium_subscriber": r.is_premium_subscriber(),
        "permissions": perms_ativas,
        "permission_count": len(perms_ativas),
        "created_at": r.created_at.isoformat(),
    }
    session.log("OK", f"Informações do cargo @{r.name} obtidas ({len(r.members)} membros)")
    return info


async def member_info(session, user_id):
    guild = session.guild
    m = guild.get_member(user_id)
    if not m:
        session.log("ERRO", f"Membro ID {user_id} não encontrado no servidor")
        return None

    info = {
        "id": m.id,
        "name": str(m),
        "display_name": m.display_name,
        "bot": m.bot,
        "status": str(m.status) if m.status else "offline",
        "joined_at": m.joined_at.isoformat() if m.joined_at else None,
        "created_at": m.created_at.isoformat(),
        "top_role": m.top_role.name if m.top_role else None,
        "top_role_id": m.top_role.id if m.top_role else None,
        "roles": [{"id": r.id, "name": r.name} for r in m.roles if not r.is_default()],
        "is_timed_out": m.is_timed_out(),
        "timed_out_until": m.timed_out_until.isoformat() if m.timed_out_until else None,
        "avatar": m.display_avatar.url,
        "joined_discord": (discord.utils.utcnow() - m.created_at).days > 30,
    }
    session.log("OK", f"Informações de {m} obtidas ({len(info['roles'])} cargos)")
    return info


async def audit_logs(session, limite=50, action=None):
    guild = session.guild
    entradas = []
    async for entry in guild.audit_logs(limit=limite):
        if action and action not in str(entry.action):
            continue
        entradas.append({
            "id": entry.id,
            "action": str(entry.action).split(".")[-1],
            "user": str(entry.user) if entry.user else None,
            "user_id": entry.user.id if entry.user else None,
            "target": str(entry.target) if entry.target else None,
            "target_id": entry.target.id if entry.target else None,
            "reason": entry.reason,
            "created_at": entry.created_at.isoformat(),
            "category": str(entry.category).split(".")[-1],
        })
    session.log("OK", f"{len(entradas)} logs de auditoria obtidos (filtro: {action or 'todos'})")
    return entradas


async def list_bans(session):
    guild = session.guild
    bans = []
    async for entry in guild.bans():
        bans.append({
            "user_id": entry.user.id,
            "user_name": str(entry.user),
            "reason": entry.reason,
        })
    session.log("OK", f"{len(bans)} banimentos listados")
    return bans


async def guild_emojis(session):
    guild = session.guild
    emojis = []
    for e in guild.emojis:
        emojis.append({
            "id": e.id,
            "name": e.name,
            "animated": e.animated,
            "url": str(e.url),
        })
    session.log("OK", f"{len(emojis)} emojis listados")
    return emojis


async def channels_by_category(session):
    guild = session.guild
    estrutura = {}
    for cat in guild.categories:
        estrutura[cat.name] = {
            "category_id": cat.id,
            "position": cat.position,
            "channels": [
                {
                    "id": ch.id,
                    "name": ch.name,
                    "type": str(ch.type).split(".")[-1],
                    "position": ch.position,
                }
                for ch in cat.channels
            ],
        }
    sem_categoria = [
        {
            "id": ch.id,
            "name": ch.name,
            "type": str(ch.type).split(".")[-1],
        }
        for ch in guild.channels
        if ch.category is None and not isinstance(ch, discord.CategoryChannel)
    ]
    if sem_categoria:
        estrutura["Sem Categoria"] = {"channels": sem_categoria}
    session.log("OK", f"Estrutura do servidor obtida ({len(estrutura)} categorias)")
    return estrutura


async def search_messages(session, channel_id, palavra, limite=100):
    guild = session.guild
    channel = guild.get_channel(channel_id)
    if not channel:
        session.log("ERRO", f"Canal ID {channel_id} não encontrado")
        return []

    palavra_lower = palavra.lower()
    encontradas = []
    async for msg in channel.history(limit=limite):
        if palavra_lower in msg.content.lower():
            encontradas.append({
                "id": msg.id,
                "author": str(msg.author),
                "author_id": msg.author.id,
                "content": msg.content[:500],
                "timestamp": msg.created_at.isoformat(),
                "jump_url": msg.jump_url,
            })

    session.log("OK", f"{len(encontradas)} mensagens com '{palavra}' em #{channel.name}")
    return encontradas


async def role_hierarchy(session):
    guild = session.guild
    hierarquia = []
    for r in sorted(guild.roles, key=lambda x: x.position, reverse=True):
        if r.is_default():
            continue
        hierarquia.append({
            "id": r.id,
            "name": r.name,
            "position": r.position,
            "color": str(r.color),
            "member_count": len(r.members),
        })
    session.log("OK", f"Hierarquia de cargos obtida ({len(hierarquia)} cargos)")
    return hierarquia


async def member_activity(session, user_id, canais_ids=None, limite_por_canal=20):
    guild = session.guild
    member = guild.get_member(user_id)
    if not member:
        session.log("ERRO", f"Membro ID {user_id} não encontrado")
        return None

    canais = []
    if canais_ids:
        for cid in canais_ids:
            ch = guild.get_channel(cid)
            if ch:
                canais.append(ch)
    else:
        canais = guild.text_channels[:5]

    atividade = []
    for ch in canais:
        count = 0
        async for msg in ch.history(limit=limite_por_canal):
            if msg.author.id == user_id:
                atividade.append({
                    "channel": ch.name,
                    "channel_id": ch.id,
                    "content": msg.content[:300],
                    "timestamp": msg.created_at.isoformat(),
                    "jump_url": msg.jump_url,
                })
                count += 1
                if count >= 10:
                    break

    session.log("OK", f"{len(atividade)} mensagens recentes de {member} em {len(canais)} canais")
    return {"member": str(member), "member_id": user_id, "recent_messages": atividade}


async def role_summary(session):
    guild = session.guild
    resumo = []
    for r in sorted(guild.roles, key=lambda x: x.position, reverse=True):
        if r.is_default():
            continue
        resumo.append({
            "id": r.id,
            "name": r.name,
            "color": str(r.color),
            "position": r.position,
            "member_count": len(r.members),
            "permission_flags": [p for p, v in dict(r.permissions) if v],
        })
    session.log("OK", f"Resumo de {len(resumo)} cargos gerado")
    return resumo
