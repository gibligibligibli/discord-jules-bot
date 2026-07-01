# Aprendizados Operacionais do Jules

1. **Intents e APIs do Discord**:
   - Ao lidar com permissões do Discord.py, lembre-se que algumas exigem `PrivilegedIntents`. Se não tiver acesso ao painel de desenvolvedor, mude `message_content` e `members` para `False` via código, caso não sejam estritamente necessários para a operação.

2. **Canais e Categorias**:
   - A função `create_channel` precisa tratar o tipo `category` especificamente utilizando `create_category`. Usar o default fará com que seja criado um canal de texto genérico.
   - Para que canais do tipo `announcement` funcionem na sua completude (com o botão de Seguir), o servidor **deve** ter a funcionalidade "COMMUNITY" habilitada.

3. **Logs Dinâmicos**:
   - Para providenciar feedback em "tempo real", enviar a mensagem inicial ("Em andamento") guardando a sua referência, e depois usar `message.edit()` é muito mais limpo do que floodar o canal com mensagens de start e finish para cada tarefa.

4. **Prevenção de Spam**:
   - Sempre verifique o histórico recente do canal (usando `channel.history`) antes de enviar mensagens automatizadas (templates) para evitar duplicação em caso de execuções múltiplas.
