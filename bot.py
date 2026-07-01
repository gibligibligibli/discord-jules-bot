"""
Executor de sessão Discord — Jules
Modo de uso: python bot.py <arquivo_de_tarefas.json>
Conecta, executa as tarefas, salva logs e desliga.
"""

import sys
import json
import os
import asyncio
from core import SessionBot, channels, roles, members, inspect, permissions


ACTION_MAP = {
    "create_channel":              channels.create,
    "edit_channel":                channels.edit,
    "delete_channel":              channels.delete,
    "list_channels":               channels.list_channels,
    "create_role":                 roles.create,
    "edit_role":                   roles.edit,
    "delete_role":                 roles.delete,
    "list_roles":                  roles.list_roles,
    "timeout":                     members.timeout,
    "remove_timeout":              members.remove_timeout,
    "kick":                        members.kick,
    "ban":                         members.ban,
    "get_messages":                members.get_messages,
    "list_members":                members.list_members,
    "guild_info":                  inspect.guild_info,
    "channel_info":                inspect.channel_info,
    "role_info":                   inspect.role_info,
    "member_info":                 inspect.member_info,
    "audit_logs":                  inspect.audit_logs,
    "list_bans":                   inspect.list_bans,
    "guild_emojis":                inspect.guild_emojis,
    "channels_by_category":        inspect.channels_by_category,
    "search_messages":             inspect.search_messages,
    "role_hierarchy":              inspect.role_hierarchy,
    "member_activity":             inspect.member_activity,
    "role_summary":                inspect.role_summary,
    "set_channel_permissions":     permissions.set_channel_permissions,
    "sync_channel_permissions":    permissions.sync_channel_permissions,
    "get_channel_overwrites":      permissions.get_channel_overwrites,
}


def carregar_tarefas(caminho):
    with open(caminho, "r", encoding="utf-8") as f:
        return json.load(f)


async def executar_sessao(token, guild_id, tarefas, caminho_resultado):
    session = SessionBot(guild_id)

    async def handler(s):
        s.log("INFO", f"Sessão iniciada no servidor: {s.guild.name}")
        for i, task in enumerate(tarefas, 1):
            action = task.get("action")
            params = task.get("params", {})
            nome = f"Tarefa {i}: {action}"
            print(f"\n--- {nome} ---")

            if action not in ACTION_MAP:
                s.log("ERRO", f"Ação desconhecida: {action}")
                continue

            try:
                resultado = await ACTION_MAP[action](s, **params)
                if resultado is not None and action in ("list_channels", "list_roles", "list_members",
                                                        "get_messages", "guild_info", "channel_info",
                                                        "role_info", "member_info", "audit_logs",
                                                        "list_bans", "guild_emojis",
                                                        "channels_by_category", "search_messages",
                                                        "role_hierarchy", "member_activity",
                                                        "role_summary", "get_channel_overwrites"):
                    s.log("OK", f"Resultado: {json.dumps(resultado, ensure_ascii=False, default=str)[:500]}")
            except Exception as e:
                s.log("FALHA", f"{action}: {e}")

        s.save_results(caminho_resultado)
        print(f"\nSessão concluída. {len([r for r in s.results if r['status'] == 'OK'])} OK, "
              f"{len([r for r in s.results if r['status'] == 'ERRO'])} erros, "
              f"{len([r for r in s.results if r['status'] == 'FALHA'])} falhas.")
        await s.close()

    session.on_ready = handler
    await session.run(token)


def main():
    if len(sys.argv) < 2:
        print("Uso: python bot.py <arquivo_de_tarefas.json>")
        sys.exit(1)

    caminho_tarefas = sys.argv[1]
    if not os.path.exists(caminho_tarefas):
        print(f"Arquivo não encontrado: {caminho_tarefas}")
        sys.exit(1)

    dados = carregar_tarefas(caminho_tarefas)
    token = os.getenv("DISCORD_TOKEN")
    if not token:
        print("Token não encontrado. Defina DISCORD_TOKEN como variável de ambiente.")
        sys.exit(1)

    guild_id = dados.get("guild_id")
    if not guild_id:
        print("Campo 'guild_id' obrigatório no JSON.")
        sys.exit(1)

    nome_sessao = dados.get("session", "sessao")
    tarefas = dados.get("tasks", [])
    caminho_resultado = f"operations/execution/{nome_sessao}_resultado.json"

    print(f"Sessão: {nome_sessao}")
    print(f"Servidor ID: {guild_id}")
    print(f"Tarefas: {len(tarefas)}")
    print(f"Resultado: {caminho_resultado}\n")

    asyncio.run(executar_sessao(token, guild_id, tarefas, caminho_resultado))


if __name__ == "__main__":
    main()
