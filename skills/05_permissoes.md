# Habilidade: Gerenciamento de Permissões

## Descrição
Define permissões específicas para cargos ou membros em canais, e sincroniza com a categoria.

## Script vinculado
`core/permissions.py` — **IMUTÁVEL**

## Ações disponíveis

### `set_channel_permissions`
Define permissões de um cargo ou membro em um canal específico.

| Parâmetro | Tipo | Obrigatório | Descrição |
|-----------|------|-------------|-----------|
| `channel_id` | int | sim | ID do canal |
| `target_id` | int | sim | ID do cargo ou membro alvo |
| `target_type` | string | sim | `"role"` ou `"member"` |
| `allow` | array | não | Lista de permissões para **permitir** |
| `deny` | array | não | Lista de permissões para **negar** |

### `sync_channel_permissions`
Sincroniza as permissões de um canal com as da sua categoria.

| Parâmetro | Tipo | Obrigatório |
|-----------|------|-------------|
| `channel_id` | int | sim |

### `get_channel_overwrites`
Lista todas as permissões especiais de um canal.

| Parâmetro | Tipo | Obrigatório |
|-----------|------|-------------|
| `channel_id` | int | sim |

## Permissões comuns
`send_messages`, `read_messages`, `view_channel`, `manage_messages`,
`attach_files`, `embed_links`, `add_reactions`, `use_external_emoji`,
`mention_everyone`, `connect`, `speak`, `manage_webhooks`,
`create_instant_invite`, `manage_channels`

## Regras para Jules
1. Nunca remover permissões de administradores.
2. Usar `get_channel_overwrites` antes de modificar para entender o estado atual.
3. Sincronizar com categoria após criar canais novos.
4. **NÃO** alterar `core/permissions.py`.

## Exemplos
```json
{ "action": "set_channel_permissions", "params": { "channel_id": 123456789, "target_id": 987654321, "target_type": "role", "allow": ["read_messages", "send_messages"], "deny": ["mention_everyone"] } }
{ "action": "sync_channel_permissions", "params": { "channel_id": 123456789 } }
{ "action": "get_channel_overwrites", "params": { "channel_id": 123456789 } }
```
