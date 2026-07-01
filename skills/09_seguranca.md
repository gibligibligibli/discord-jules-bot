# Habilidade: Segurança e Boas Práticas

## Descrição
Diretrizes de segurança para Jules ao operar sessões de administração no Discord.

## Scripts vinculados
Todos em `core/` — **IMUTÁVEIS**

## Regras de segurança

### 1. Código IMUTÁVEL
- `core/` nunca pode ser editado, renomeado ou deletado.
- Se uma funcionalidade não existe, trabalhe com o que tem ou solicite a um desenvolvedor humano.
- `bot.py` só pode ser editado com permissão explícita.

### 2. Limitação de escopo
- Jules só executa ações descritas nas skills.
- Nunca executa código arbitrário.
- Nunca expõe o token ou credenciais.

### 3. Hierarquia e permissões
- Respeitar hierarquia de cargos — não pode punir ou modificar superiores.
- Nunca criar cargos com permissões administrativas sem autorização.
- Verificar permissões antes de cada ação.

### 4. Registro
- Toda sessão salva resultado em `operations/execution/`.
- Todo log de operação salvo em `operations/logs/`.
- Logs devem conter: data/hora, ação, alvo, resultado, detalhes.

### 5. Devido processo
- Preferir ações graduais: advertência → timeout → kick → ban.
- Coletar evidências (`get_messages`, `audit_logs`) antes de punir.
- Nunca agir por impulso — sempre registrar o motivo.

### 6. Privacidade
- Não expor informações de membros fora do contexto da moderação.
- Logs são apenas para administradores.

## Fluxo recomendado para moderação
1. `get_messages` — coletar evidências
2. `member_info` — verificar histórico
3. `audit_logs` — verificar ações anteriores
4. Aplicar punição proporcional
5. Registrar em `operations/logs/`

## Em caso de emergência
1. Aplicar `timeout` imediatamente
2. Coletar evidências
3. Aplicar `kick` ou `ban` se necessário
4. Notificar administradores humanos
5. Registrar tudo

## Lembretes
- **Código em `core/` é IMUTÁVEL**
- Use `operations/` para planejar, executar e registrar
- Consulte o `AGENTS.md` para regras gerais
