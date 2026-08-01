---
name: revise-concept
description: Registra e aplica uma revisão por prompt sem sobrescrever versões.
argument-hint: <project_id> <room_id>
disable-model-invocation: true
---

Projeto e ambiente: `$ARGUMENTS`

Converta o pedido da arquiteta em:
- alterações;
- elementos preservados;
- requisitos novos;
- requisitos substituídos;
- possíveis conflitos.

Crie revisão numerada em `docs/clients/<project_id>/revisions`.
Atualize prompts, gere nova versão e rode auditoria de regressão.
