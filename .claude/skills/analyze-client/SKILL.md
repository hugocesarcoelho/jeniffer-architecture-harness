---
name: analyze-client
description: Executa intake e análise espacial de um projeto de cliente.
argument-hint: <project_id>
disable-model-invocation: true
---

Projeto: `$ARGUMENTS`

1. execute `python scripts/harness.py validate --client $ARGUMENTS`;
2. use `intake-analyst`;
3. use `spatial-analyst`;
4. grave resultados em `docs/clients/$ARGUMENTS/output/analysis`;
5. não prossiga se houver erros bloqueantes;
6. apresente resumo de requisitos, conflitos e ausências.
