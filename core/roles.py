import discord

CORES_MAP = {
    "azul": discord.Color.blue(), "vermelho": discord.Color.red(),
    "verde": discord.Color.green(), "amarelo": discord.Color.gold(),
    "roxo": discord.Color.purple(), "laranja": discord.Color.orange(),
    "preto": discord.Color.default(), "branco": discord.Color.from_rgb(255, 255, 255),
    "cinza": discord.Color.light_gray(), "rosa": discord.Color.magenta(),
}

async def create(session, nome, cor=None, exibicao_separada=False, mencao_permitida=False, permissoes=None):
    guild = session.guild
    kwargs = {"name": nome, "reason": "Jules session: criar cargo"}

    if cor:
        kwargs["color"] = CORES_MAP.get(cor.lower(), discord.Color.default())

    kwargs["hoist"] = exibicao_separada
    kwargs["mentionable"] = mencao_permitida

    if permissoes:
        perms = discord.Permissions()
        for perm, valor in permissoes.items():
            if hasattr(perms, perm):
                setattr(perms, perm, valor)
        kwargs["permissions"] = perms

    cargo = await guild.create_role(**kwargs)
    session.log("OK", f"Cargo @{cargo.name} criado (ID: {cargo.id})")
    return cargo


async def edit(session, role_id, nome=None, cor=None, exibicao_separada=None, mencao_permitida=None, permissoes=None):
    guild = session.guild
    cargo = guild.get_role(role_id)
    if not cargo:
        session.log("ERRO", f"Cargo ID {role_id} não encontrado")
        return None

    kwargs = {}
    if nome is not None:
        kwargs["name"] = nome
    if cor is not None:
        kwargs["color"] = CORES_MAP.get(cor.lower(), discord.Color.default())
    if exibicao_separada is not None:
        kwargs["hoist"] = exibicao_separada
    if mencao_permitida is not None:
        kwargs["mentionable"] = mencao_permitida
    if permissoes:
        perms = cargo.permissions
        for perm, valor in permissoes.items():
            if hasattr(perms, perm):
                setattr(perms, perm, valor)
        kwargs["permissions"] = perms

    if kwargs:
        await cargo.edit(**kwargs, reason="Jules session: editar cargo")

    session.log("OK", f"Cargo @{cargo.name} editado ({', '.join(kwargs.keys())})")
    return cargo


async def delete(session, role_id):
    guild = session.guild
    cargo = guild.get_role(role_id)
    if not cargo:
        session.log("ERRO", f"Cargo ID {role_id} não encontrado")
        return
    nome = cargo.name
    await cargo.delete(reason="Jules session: deletar cargo")
    session.log("OK", f"Cargo @{nome} deletado")


async def list_roles(session):
    guild = session.guild
    cargos = []
    for r in sorted(guild.roles, key=lambda x: x.position, reverse=True):
        if r.is_default():
            continue
        cargos.append({
            "id": r.id,
            "name": r.name,
            "color": str(r.color),
            "position": r.position,
            "member_count": len(r.members),
        })
    session.log("OK", f"{len(cargos)} cargos listados")
    return cargos
