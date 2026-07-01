# Habilidade: Moderação de Membros

## Descrição
Aplica timeout, expulsa, bane, obtém mensagens e lista membros do servidor.

## Script vinculado
`core/members.py` — **IMUTÁVEL**

## Ações disponíveis

### `timeout`
Silencia um membro por tempo determinado.

| Parâmetro | Tipo | Obrigatório | Descrição |
|-----------|------|-------------|-----------|
| `user_id` | int | sim | ID do usuário |
| `minutos` | int | sim | Duração em minutos |
| `motivo` | string | não | Motivo do silenciamento |

### `remove_timeout`
Remove o silenciamento de um membro.

| Parâmetro | Tipo | Obrigatório |
|-----------|------|-------------|
| `user_id` | int | sim |

### `kick`
Expulsa um membro do servidor.

| Parâmetro | Tipo | Obrigatório | Descrição |
|-----------|------|-------------|-----------|
| `user_id` | int | sim | ID do usuário |
| `motivo` | string | não | Motivo |

### `ban`
Bane um usuário do servidor (funciona mesmo se ele não estiver mais no servidor).

| Parâmetro | Tipo | Obrigatório | Descrição |
|-----------|------|-------------|-----------|
| `user_id` | int | sim | ID do usuário |
| `motivo` | string | não | Motivo |
| `dias_excluir_mensagens` | int | não | Dias de mensagens para apagar (0-7) |

### `get_messages`
Obtém mensagens de um canal, opcionalmente filtradas por usuário.

| Parâmetro | Tipo | Obrigatório | Descrição |
|-----------|------|-------------|-----------|
| `channel_id` | int | sim | ID do canal |
| `user_id` | int | não | Filtrar por usuário |
| `limite` | int | não | Máximo de mensagens (padrão: 100) |

### `list_members`
Lista membros do servidor, opcionalmente filtrados por cargo.

| Parâmetro | Tipo | Obrigatório | Descrição |
|-----------|------|-------------|-----------|
| `cargo_id` | int | não | Filtrar por cargo |

## Regras para Jules
1. Preferir `timeout` como primeira ação corretiva antes de `kick` ou `ban`.
2. Sempre registrar o motivo.
3. Não banir/expulsar sem justificativa clara e registrada.
4. Usar `get_messages` para coletar evidências antes de punir.
5. **NÃO** alterar `core/members.py`.

## Exemplos
```json
{ "action": "timeout", "params": { "user_id": 123456789, "minutos": 30, "motivo": "Spam excessivo no chat geral" } }
{ "action": "get_messages", "params": { "channel_id": 123456789, "user_id": 123456789, "limite": 20 } }
{ "action": "kick", "params": { "user_id": 123456789, "motivo": "Violação de regras após 3 advertências" } }
{ "action": "ban", "params": { "user_id": 123456789, "motivo": "Conta de spam", "dias_excluir_mensagens": 1 } }
{ "action": "list_members", "params": { "cargo_id": 987654321 } }
```
