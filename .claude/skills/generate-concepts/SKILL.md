---
name: generate-concepts
description: Gera especificações, prompts e imagens conceituais de todos os ambientes.
argument-hint: <project_id>
disable-model-invocation: true
---

Projeto: `$ARGUMENTS`

1. confirme análise concluída;
2. use `concept-designer`;
3. execute `python scripts/harness.py build-prompts --client $ARGUMENTS`;
4. execute `python scripts/harness.py render --client $ARGUMENTS`;
5. use `requirement-auditor`;
6. salve tudo em `docs/clients/$ARGUMENTS/output`;
7. informe claramente quando o provider estiver em modo mock.
