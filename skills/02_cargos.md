# Habilidade: Gerenciamento de Cargos

## Descrição
Cria, edita, deleta e lista cargos do servidor.

## Script vinculado
`core/roles.py` — **IMUTÁVEL**

## Ações disponíveis

### `create_role`
Cria um novo cargo.

| Parâmetro | Tipo | Obrigatório | Descrição |
|-----------|------|-------------|-----------|
| `nome` | string | sim | Nome do cargo |
| `cor` | string | não | `azul`, `vermelho`, `verde`, `amarelo`, `roxo`, `laranja`, `rosa`, `cinza`, `branco`, `preto` |
| `exibicao_separada` | bool | não | Exibir separado na lista? |
| `mencao_permitida` | bool | não | Permitir @menção? |
| `permissoes` | object | não | Dict de permissões (ex: `{"kick_members": true}`) |

### `edit_role`
Edita um cargo existente (mesmos parâmetros de `create_role` + `role_id`).

| Parâmetro | Tipo | Obrigatório | Descrição |
|-----------|------|-------------|-----------|
| `role_id` | int | sim | ID do cargo |

### `delete_role`
Deleta um cargo.

| Parâmetro | Tipo | Obrigatório | Descrição |
|-----------|------|-------------|-----------|
| `role_id` | int | sim | ID do cargo |

### `list_roles`
Lista todos os cargos do servidor (sem parâmetros).

## Regras para Jules
1. **NUNCA** criar cargos com permissões administrativas sem autorização explícita.
2. Não deletar cargos que estão em uso sem verificar antes.
3. Manter hierarquia — cargos mais importantes no topo.
4. **NÃO** alterar `core/roles.py`.

## Exemplos
```json
{ "action": "create_role", "params": { "nome": "Moderador", "cor": "vermelho", "exibicao_separada": true, "permissoes": { "kick_members": true, "ban_members": false, "mute_members": true } } }
{ "action": "edit_role", "params": { "role_id": 123456789, "nome": "Mod Senior", "cor": "roxo" } }
{ "action": "list_roles", "params": {} }
{ "action": "delete_role", "params": { "role_id": 123456789 } }
```
