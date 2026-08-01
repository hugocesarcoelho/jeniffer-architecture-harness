---
name: generate-detailing
description: Prepara o pacote de detalhamento e PDF preliminar após aprovação.
argument-hint: <project_id>
disable-model-invocation: true
---

Projeto: `$ARGUMENTS`

1. verifique aprovações;
2. use `detailing-editor`;
3. rode auditoria;
4. execute `python scripts/harness.py detailing --client $ARGUMENTS`;
5. informe pendências e validações técnicas.
