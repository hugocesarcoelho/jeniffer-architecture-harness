# Jeniffer Architecture Harness — Claude Code

Harness para projetos residenciais de arquitetura e design de interiores, usando Claude Code como orquestrador.

## O que este projeto faz

1. Organiza o acervo histórico de PDFs da arquiteta.
2. Extrai textos, páginas e imagens dos PDFs.
3. Constrói um **Design DNA** com padrões recorrentes da arquiteta.
4. Recebe um novo projeto estruturado por cliente e ambiente.
5. Consolida requisitos em uma especificação rastreável.
6. Gera prompts de renderização por ambiente e ângulo.
7. Envia os prompts a um provedor de imagens configurável.
8. Registra ajustes solicitados por prompt.
9. Executa auditoria entre briefing, revisões e resultados.
10. Prepara o conteúdo necessário para o PDF de detalhamento.

## Limitação importante

Claude Code é o orquestrador e o agente de análise. Ele consegue ler código, arquivos, imagens e PDFs, mas a geração de imagens renderizadas exige integração com um modelo de imagem, serviço de renderização ou ferramenta 3D externa.

Este starter inclui:

- `mock`: cria imagens-placeholder para testar o fluxo;
- `rest`: integração genérica com uma API HTTP de geração;
- interface pronta para adicionar ComfyUI, Stable Diffusion, Flux, Blender, SketchUp ou outro provedor.

Para precisão técnica de projeto executivo, as imagens de IA devem ser tratadas como **estudos conceituais**, não como desenhos construtivos definitivos. Medidas, instalações, estrutura, normas e especificações precisam de validação profissional.

## Pré-requisitos

- Python 3.11+
- Claude Code
- Git
- Opcional: API de geração de imagens

## Instalação

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
cp .env.example .env
```

No Windows PowerShell, instale o Claude Code conforme a documentação oficial da Anthropic e abra o diretório:

```powershell
claude
```

## Estrutura

```text
.
├── CLAUDE.md
├── .claude/
│   ├── agents/
│   └── skills/
├── config/
├── docs/
│   ├── knowledge-base/
│   │   ├── raw-pdfs/
│   │   ├── extracted/
│   │   └── design-dna/
│   ├── clients/
│   │   └── _template/
│   └── output/
├── schemas/
├── scripts/
└── tests/
```

## Fluxo inicial: aprender o estilo da arquiteta

Coloque os PDFs históricos em:

```text
docs/knowledge-base/raw-pdfs/
```

Execute:

```bash
python scripts/harness.py ingest-library
```

Depois, no Claude Code:

```text
/design-dna
```

O Claude analisará os artefatos extraídos e preencherá:

```text
docs/knowledge-base/design-dna/design-dna.yaml
```

Revise esse arquivo manualmente. Ele é a principal memória curada do estilo.

## Criar novo cliente

```bash
python scripts/harness.py new-client --id silva-2026 --name "Família Silva"
```

Preencha:

```text
docs/clients/silva-2026/brief/project.yaml
docs/clients/silva-2026/brief/requirements.yaml
```

Adicione arquivos:

```text
inputs/
├── floorplans/
├── references/
├── property-photos/
│   ├── sala/
│   ├── cozinha/
│   └── quarto-01/
└── supporting-documents/
```

Valide:

```bash
python scripts/harness.py validate --client silva-2026
```

No Claude Code:

```text
/analyze-client silva-2026
```

## Gerar prompts e imagens

```text
/generate-concepts silva-2026
```

Ou pela CLI:

```bash
python scripts/harness.py build-prompts --client silva-2026
python scripts/harness.py render --client silva-2026
```

As imagens são gravadas dentro da pasta do próprio cliente:

```text
docs/clients/silva-2026/output/concepts/<ambiente>/<versao>/
```

## Solicitar ajustes

No Claude Code:

```text
/revise-concept silva-2026 sala
```

Exemplo de pedido:

```text
Na imagem principal da sala:
- trocar o pendente por um modelo linear;
- manter mesa de seis lugares;
- mudar as cadeiras para suede verde oliva;
- preservar exatamente a posição da janela;
- não alterar piso nem pontos elétricos.
```

Cada revisão gera um registro em:

```text
docs/clients/<id>/revisions/
```

e uma nova versão de imagem, sem sobrescrever a anterior.

## Auditoria de requisitos

```text
/audit-project silva-2026
```

O auditor compara:

- requisitos originais;
- restrições técnicas;
- referências;
- Design DNA;
- decisões aprovadas;
- pedidos de revisão;
- prompts finais;
- inventário de imagens;
- itens do detalhamento.

Saída:

```text
docs/clients/<id>/output/audit/audit-report.md
docs/clients/<id>/output/audit/traceability-matrix.csv
```

## PDF de detalhamento

Após aprovação conceitual:

```text
/generate-detailing silva-2026
```

O harness prepara:

- memorial descritivo;
- especificação por ambiente;
- tabela de materiais;
- tabela de esquadrias;
- iluminação;
- elétrica;
- hidráulica;
- marcenaria;
- mobiliário;
- itens pendentes;
- referências às pranchas e imagens.

A geração final de prancha técnica deve ser integrada ao software de autoria da arquiteta ou a um pipeline específico de CAD/BIM/SketchUp/Layout. Este starter gera o pacote de conteúdo e um PDF textual preliminar.

## Comandos do harness

```bash
python scripts/harness.py --help
```

## Recomendação de implantação

Comece com 10 a 20 projetos históricos representativos, classificados por tipologia e qualidade. Não use todos os PDFs indiscriminadamente. Revise o Design DNA, execute dois ou três projetos-piloto e crie um conjunto de testes visuais antes de ampliar o acervo.
