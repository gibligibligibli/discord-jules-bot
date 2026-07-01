# Habilidade: Inspeção e Diagnóstico

## Descrição
Obtém informações detalhadas sobre o servidor, canais, cargos, membros, banimentos, auditoria e conteúdo. Use estas ferramentas **antes** de tomar qualquer ação para ter visibilidade completa.

## Script vinculado
`core/inspect.py` — **IMUTÁVEL**

## Ações disponíveis

### `guild_info`
Informações completas do servidor (sem parâmetros).

Retorna: nome, ID, dono, contagem de membros/online/canais/cargos, boost, nível de verificação, filtro de conteúdo, canais de sistema/regras.

### `channels_by_category`
Estrutura completa do servidor organizada por categorias (sem parâmetros).

Retorna: para cada categoria, lista de canais com ID, nome, tipo e posição. Canais sem categoria aparecem em "Sem Categoria".

### `channel_info`
Informações detalhadas de um canal específico.

| Parâmetro | Tipo | Obrigatório |
|-----------|------|-------------|
| `channel_id` | int | sim |

Retorna: nome, tipo, categoria, posição, tópico, nsfw, slowmode, membros, permissões sincronizadas.

### `role_hierarchy`
Hierarquia completa de cargos (sem parâmetros).

Retorna: lista ordenada do cargo mais alto ao mais baixo, com nome, ID, posição, cor e contagem de membros.

### `role_summary`
Resumo de todos os cargos com permissões (sem parâmetros).

Retorna: cada cargo com suas permissões ativas em formato legível.

### `role_info`
Informações detalhadas de um cargo específico.

| Parâmetro | Tipo | Obrigatório |
|-----------|------|-------------|
| `role_id` | int | sim |

Retorna: nome, cor, posição, permissões ativas, contagem de membros, se é gerenciado por bot, se é boost.

### `member_info`
Informações detalhadas de um membro.

| Parâmetro | Tipo | Obrigatório |
|-----------|------|-------------|
| `user_id` | int | sim |

Retorna: nome, status, cargos, entrou em, timeout ativo/até, idade da conta.

### `member_activity`
Mensagens recentes de um membro em vários canais. Ideal para investigar comportamento.

| Parâmetro | Tipo | Obrigatório | Descrição |
|-----------|------|-------------|-----------|
| `user_id` | int | sim | ID do membro |
| `canais_ids` | array | não | Lista de IDs de canais (padrão: primeiros 5 canais de texto) |
| `limite_por_canal` | int | não | Máx de mensagens por canal (padrão: 20) |

### `audit_logs`
Obtém o histórico de auditoria do servidor.

| Parâmetro | Tipo | Obrigatório | Descrição |
|-----------|------|-------------|-----------|
| `limite` | int | não | Quantidade de entradas (padrão: 50) |
| `action` | string | não | Filtrar por ação (ex: `ban`, `kick`, `channel_create`) |

### `list_bans`
Lista todos os usuários banidos do servidor (sem parâmetros).

Retorna: ID, nome, motivo do banimento. Útil para verificar se alguém já foi banido antes.

### `guild_emojis`
Lista todos os emojis personalizados do servidor (sem parâmetros).

### `search_messages`
Busca mensagens por palavra-chave em um canal.

| Parâmetro | Tipo | Obrigatório | Descrição |
|-----------|------|-------------|-----------|
| `channel_id` | int | sim | ID do canal |
| `palavra` | string | sim | Termo para buscar |
| `limite` | int | não | Mensagens a examinar (padrão: 100) |

## Regras para Jules
1. **Sempre** começar uma sessão com `guild_info` + `channels_by_category` para ter visão geral.
2. Antes de punir: usar `member_info`, `member_activity`, `audit_logs` para contexto completo.
3. Antes de criar/alocar: usar `role_hierarchy` e `channels_by_category`.
4. Antes de banir: usar `list_bans` para verificar se já foi banido antes.
5. Usar `search_messages` para encontrar evidências específicas.
6. **NÃO** alterar `core/inspect.py`.

## Exemplos
```json
{ "action": "guild_info", "params": {} }
{ "action": "channels_by_category", "params": {} }
{ "action": "role_hierarchy", "params": {} }
{ "action": "member_info", "params": { "user_id": 555555555 } }
{ "action": "member_activity", "params": { "user_id": 555555555, "limite_por_canal": 10 } }
{ "action": "audit_logs", "params": { "limite": 20, "action": "ban" } }
{ "action": "list_bans", "params": {} }
{ "action": "search_messages", "params": { "channel_id": 123456789, "palavra": "golpe" } }
```
