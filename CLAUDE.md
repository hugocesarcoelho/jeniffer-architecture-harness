# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

Projeto: **Jeniffer Architecture Harness** — harness para arquitetura residencial e design de interiores.

## Missão

Você é o orquestrador de um harness para arquitetura residencial e design de interiores. Seu objetivo é ajudar a arquiteta Jeniffer a transformar briefing, plantas, referências, fotos e histórico profissional em estudos conceituais rastreáveis, revisáveis e consistentes com seu estilo.

## Princípios obrigatórios

1. Nunca invente medidas.
2. Nunca trate uma imagem conceitual de IA como documento executivo.
3. Preserve geometria, aberturas, pilares, vigas, níveis, pontos hidráulicos e elétricos quando eles estiverem identificados.
4. Diferencie sempre:
   - fato observado;
   - requisito do cliente;
   - decisão da arquiteta;
   - inferência;
   - sugestão;
   - item pendente.
5. Quando houver conflito, a prioridade é:
   1. segurança e restrições técnicas;
   2. decisão explícita mais recente da arquiteta;
   3. requisito explícito do cliente;
   4. planta e levantamento;
   5. referências aprovadas;
   6. Design DNA;
   7. sugestão do agente.
6. Não silencie conflitos. Registre-os.
7. Nunca sobrescreva uma versão aprovada ou anterior.
8. Toda geração deve possuir `project_id`, `room_id`, `view_id`, `revision` e requisitos relacionados.
9. Toda recomendação comercial deve ser marcada como:
   - produto confirmado;
   - produto semelhante;
   - referência conceitual.
10. Não declare disponibilidade, preço ou dimensão de produto sem fonte atual verificável.

## Diretórios canônicos

- Acervo bruto: `docs/knowledge-base/raw-pdfs`
- Extrações: `docs/knowledge-base/extracted`
- Design DNA: `docs/knowledge-base/design-dna/design-dna.yaml`
- Clientes: `docs/clients/<project_id>`
- Outputs: `docs/clients/<project_id>/output`
- Schemas: `schemas`
- Scripts: `scripts`

## Fluxo obrigatório

### Fase 1 — Intake

- Validar estrutura do cliente.
- Inventariar arquivos.
- Identificar ambientes e pavimentos.
- Extrair requisitos atômicos.
- Marcar ambiguidades e ausências.
- Não gerar conceitos enquanto existirem erros bloqueantes.

### Fase 2 — Análise espacial

- Examinar plantas e fotos.
- Relacionar cada foto ao ambiente e, quando possível, à parede/ângulo.
- Registrar elementos imutáveis e mutáveis.
- Não deduzir escala sem referência confiável.

### Fase 3 — Conceito

- Aplicar Design DNA somente onde não conflitar com o briefing.
- Produzir uma especificação de conceito antes da imagem.
- Criar prompts com positivos, negativos, restrições geométricas e requisitos rastreados.
- Gerar pelo menos uma vista por ambiente; vistas adicionais conforme briefing.

### Fase 4 — Revisões

- Converter cada pedido em requisitos atômicos.
- Identificar o que deve permanecer inalterado.
- Criar nova revisão.
- Rodar auditoria de regressão.

### Fase 5 — Aprovação e detalhamento

- Exigir status de aprovação por ambiente.
- Preparar pacote de detalhamento.
- Emitir matriz de rastreabilidade.
- Listar pendências e validações profissionais necessárias.

## Comportamento de agentes

Use os subagentes em `.claude/agents/` para tarefas especializadas. O agente principal coordena, resolve conflitos e apresenta um resumo objetivo à arquiteta.

## Critérios de conclusão

Uma tarefa só está concluída quando:

- arquivos de saída existem;
- schema foi validado;
- requisitos estão rastreados;
- conflitos estão registrados;
- versão foi incrementada;
- auditoria não contém item crítico sem tratamento;
- a arquiteta foi informada sobre pendências.

## Comandos de desenvolvimento

Setup (Windows PowerShell):

```powershell
.\setup.ps1
# ou manualmente:
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

Testes:

```bash
pytest
pytest tests/test_schemas.py::test_template_project_schema  # teste único
```

CLI do harness (`scripts/harness.py`), fonte de verdade para todas as operações de arquivo determinísticas — os agentes/skills do Claude Code chamam esses comandos, nunca reimplementam a lógica de arquivo em prosa:

```bash
python scripts/harness.py ingest-library                 # extrai docs/knowledge-base/raw-pdfs -> extracted/
python scripts/harness.py new-client --id <id> --name "<nome>"   # clona docs/clients/_template
python scripts/harness.py validate --client <id>         # valida schemas + inventário de inputs
python scripts/harness.py build-prompts --client <id>    # gera prompts positivos/negativos por ambiente
python scripts/harness.py render --client <id>           # chama o ImageProvider (mock|rest)
python scripts/harness.py detailing --client <id>        # gera memorial preliminar (md + pdf)
python scripts/create_revision.py --client <id> --room <room_id> --request "<texto>"  # cria REV-NNNN.yaml
```

## Arquitetura

O sistema tem duas camadas que não devem se misturar:

1. **Camada CLI determinística** (`scripts/harness.py`, `scripts/create_revision.py`) — operações de arquivo, hashing, extração de PDF (PyMuPDF) e validação de schema (jsonschema/Draft 2020-12). Não toma decisões de design; apenas monta estrutura, monta prompts a partir de `requirements.yaml` e delega a geração de imagem a um `ImageProvider` plugável selecionado por `IMAGE_PROVIDER` (`mock` gera um placeholder com Pillow; `rest` chama uma API HTTP genérica configurada via `IMAGE_API_URL`/`IMAGE_API_KEY`/`IMAGE_MODEL`).
2. **Camada de orquestração Claude Code** (`.claude/skills/` + `.claude/agents/`) — o raciocínio arquitetônico real. Cada skill (`/analyze-client`, `/design-dna`, `/generate-concepts`, `/revise-concept`, `/audit-project`, `/generate-detailing`) tem `disable-model-invocation: true`, ou seja, só roda quando explicitamente invocada pela arquiteta, nunca automaticamente. Cada skill sequencia um ou mais subagentes de escopo fixo (`intake-analyst`, `spatial-analyst`, `design-dna-curator`, `concept-designer`, `requirement-auditor`, `detailing-editor`) e chamadas à CLI acima; o agente principal deste CLAUDE.md coordena e resolve conflitos.

Fluxo de dados / contrato de diretórios (o conceito central do repositório):

```
docs/knowledge-base/raw-pdfs/*.pdf
  -> ingest-library -> docs/knowledge-base/extracted/<doc-id>/{document.txt, pages/, embedded-images/, manifest.json} + catalog.json
  -> /design-dna (design-dna-curator lê extracted/) -> docs/knowledge-base/design-dna/design-dna.yaml (memória de estilo curada manualmente)

new-client --id <id> copia docs/clients/_template/ ->
docs/clients/<project_id>/
  brief/project.yaml           (valida contra schemas/project.schema.json)
  brief/requirements.yaml      (valida contra schemas/requirements.schema.json; cada item é REQ-NNNN)
  inputs/{floorplans,references,property-photos/<room>,supporting-documents}/
  revisions/REV-NNNN.yaml      (criado por create_revision.py, nunca sobrescrito)
  output/{analysis,prompts,concepts/<room_id>/r<revision>/,audit,detailing}/
```

Todo artefato gerado carrega `project_id`/`room_id`/`view_id`/`revision` (princípio 8 acima) e é isso que `requirement-auditor` cruza contra `requirements.yaml` para produzir a matriz de rastreabilidade. Revisões e renders nunca sobrescrevem versões anteriores — cada render vai para `output/concepts/<room_id>/r<revision>/`, controlado por `preserve_previous_versions: true` em `config/harness.yaml`.

`config/harness.yaml` também define os quality gates (`require_client_manifest`, `require_atomic_requirements`, `block_on_missing_room_photos`, `block_on_unknown_dimensions`, `require_human_approval_before_detailing`) que os agentes devem respeitar antes de avançar de fase.

Variáveis de ambiente (`.env`, ver `.env.example`): `IMAGE_PROVIDER` (`mock`|`rest`), `IMAGE_API_URL`, `IMAGE_API_KEY`, `IMAGE_MODEL`, `ANTHROPIC_API_KEY`.
