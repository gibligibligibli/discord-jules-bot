# Habilidade: Sessões de Administração

## Descrição
Jules executa tarefas administrativas no Discord por **sessões**: conecta, executa todas as tarefas de uma vez, salva os logs e desliga.

## Como funciona
1. Jules cria um arquivo JSON em `operations/tasks/` com a lista de tarefas
2. Executa: `python bot.py operations/tasks/meu_task.json`
3. O bot conecta ao Discord, executa cada tarefa em sequência
4. Salva o resultado em `operations/execution/`
5. Desliga automaticamente

## Formato do arquivo de tarefas

```json
{
  "session": "nome-da-sessao",
  "guild_id": 123456789012345678,
  "tasks": [
    { "action": "acao", "params": { "param1": "valor1", ... } },
    { "action": "outra_acao", "params": { ... } }
  ]
}
```

| Campo | Descrição |
|-------|-----------|
| `session` | Nome único para identificar a sessão |
| `guild_id` | ID numérico do servidor Discord |
| `tasks` | Array de tarefas a executar em ordem |

## Script vinculado
`bot.py` — ponto de entrada. Lê o JSON, executa, desliga.

## Regras para Jules
1. Sempre testar com `channel_info` ou `guild_info` antes de modificar.
2. Cada arquivo de tarefa = uma sessão completa.
3. Revisar o resultado em `operations/execution/` após cada sessão.
4. **NUNCA** editar arquivos dentro de `core/`.
5. Logar cada operação em `operations/logs/`.

## Exemplo completo
```json
{
  "session": "2026-07-01-consolidacao",
  "guild_id": 123456789012345678,
  "tasks": [
    { "action": "guild_info", "params": {} },
    { "action": "list_channels", "params": {} }
  ]
}
```

Para rodar: `$env:DISCORD_TOKEN="seu_token"; python bot.py operations/tasks/meu_task.json`
