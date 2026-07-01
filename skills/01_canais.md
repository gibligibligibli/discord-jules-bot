# Habilidade: Gerenciamento de Canais

## Descrição
Cria, edita, deleta e lista canais do servidor.

## Script vinculado
`core/channels.py` — **IMUTÁVEL**

## Ações disponíveis

### `create_channel`
Cria um novo canal.

| Parâmetro | Tipo | Obrigatório | Descrição |
|-----------|------|-------------|-----------|
| `nome` | string | sim | Nome do canal |
| `tipo` | string | não | `text` (padrão), `voice`, `forum`, `announcement` |
| `categoria` | string | não | Nome da categoria (cria se não existir) |
| `topico` | string | não | Descrição do canal |

### `edit_channel`
Edita um canal existente.

| Parâmetro | Tipo | Obrigatório | Descrição |
|-----------|------|-------------|-----------|
| `channel_id` | int | sim | ID do canal |
| `nome` | string | não | Novo nome |
| `topico` | string | não | Novo tópico |
| `categoria` | string | não | Nova categoria |
| `posicao` | int | não | Posição na lista |
| `nsfw` | bool | não | Canal adulto? |
| `slowmode_delay` | int | não | Slowmode em segundos |

### `delete_channel`
Deleta um canal.

| Parâmetro | Tipo | Obrigatório | Descrição |
|-----------|------|-------------|-----------|
| `channel_id` | int | sim | ID do canal |

### `list_channels`
Lista todos os canais do servidor (sem parâmetros).

## Regras para Jules
1. Nunca deletar `#geral` ou canais importantes sem confirmação.
2. Preferir nomes em minúsculo com hífen (ex: `central-de-ajuda`).
3. Verificar se o canal já existe antes de criar.
4. **NÃO** alterar `core/channels.py`.

## Exemplos
```json
{ "action": "create_channel", "params": { "nome": "projetos", "tipo": "text", "categoria": "TRABALHO", "topico": "Discussão de projetos" } }
{ "action": "edit_channel", "params": { "channel_id": 123456789, "nome": "projetos-2026", "topico": "Atualizado" } }
{ "action": "list_channels", "params": {} }
{ "action": "delete_channel", "params": { "channel_id": 123456789 } }
```
