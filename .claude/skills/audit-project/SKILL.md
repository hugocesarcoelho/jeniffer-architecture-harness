---
name: audit-project
description: Executa auditoria criteriosa de cobertura e rastreabilidade.
argument-hint: <project_id>
disable-model-invocation: true
---

Use `requirement-auditor` para o projeto `$ARGUMENTS`.

Gere:
- `audit-report.md`;
- `traceability-matrix.csv`;
- `missing-items.yaml`;
- resumo para a arquiteta.

Itens ausentes devem ser propostos, nunca ocultados.
