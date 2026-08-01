# Evidence Report — Design DNA (Jeniffer Melo Arquitetura)

Data: 2026-08-01
Status do Design DNA associado: `in-review` (rascunho preliminar, pendente de validação da arquiteta)

## 0. Changelog / cronologia

- **v1/v2 (curadoria anterior)**: Design DNA construído a partir de 18 documentos de 8 `client_project`. A categoria comercial/residencial de cada projeto era **inferida do conteúdo** dos documentos (menções a "clínica", "loja", nomes de ambiente, etc.), não fornecida diretamente pela arquiteta.
- **v3 (esta curadoria)**: A arquiteta reorganizou o acervo bruto em `docs/knowledge-base/raw-pdfs/Comercial/<projeto>/` e `docs/knowledge-base/raw-pdfs/Residencial/<projeto>/`. O `ingest-library` foi reexecutado e agora todo documento em `catalog.json`/`manifest.json` carrega um campo explícito e autoritativo `project_category` ("Comercial" ou "Residencial"). Os `document_id` também mudaram (prefixo por categoria, ex. `comercial-clinicapatricia-2026-...`, `residencial-gabi-2024-...`). Esta versão **releu o catálogo do zero** e recalculou os padrões usando essa categorização explícita, com foco em: (a) separar claramente o que é padrão residencial, comercial ou de ambos os segmentos; (b) sinalizar padrões observados apenas nos 2 projetos comerciais como não-generalizáveis, mesmo quando tecnicamente atingem o piso numérico de "confiança média"; (c) corrigir algumas atribuições de projeto que se mostraram equivocadas ao re-verificar diretamente o texto extraído (ver seção 6).
- Os 8 `client_project` e a contagem de documentos são os mesmos da v2 — o que mudou é a fonte de verdade da categorização (autoritativa vs. inferida) e o nível de granularidade da análise por segmento, não a amostra em si.

## 1. Metodologia

1. Fonte: `docs/knowledge-base/extracted/`, contendo 18 documentos técnicos (`document.txt` extraído de PDF + imagens de página) provenientes de 8 pastas de cliente (`client_project`) distintas, listadas em `docs/knowledge-base/extracted/catalog.json`.
2. Categoria de cada projeto confirmada diretamente no `catalog.json` (campo `project_category`, presente em todos os 18 registros de documento): **Comercial** para ClinicaPatricia-2026 e Tavora-2026 (5 documentos); **Residencial** para Clodoaldo-Vanusa-2025, Debora-Deivisson-2026, Gabi-2024, Patricia-Rafael-2025, Rafael-Mariana-2026 e Sandra (13 documentos).
3. Para cada termo de material/cor/iluminação/marcenaria/composição candidato a padrão, foi feita busca em `document.txt` de cada documento e contado: (a) número de ocorrências, (b) `client_project` distintos com pelo menos 1 ocorrência, (c) — **novo nesta passada** — se a ocorrência está em um `client_project` **Comercial**, **Residencial**, ou ambos.
4. Regra de confiança:
   - **Alta confiança**: padrão presente em ≥ 3 `client_project` distintos.
   - **Confiança média**: padrão presente em exatamente 2 `client_project` distintos.
   - **Evidência insuficiente / preferência do cliente**: padrão presente em apenas 1 `client_project`.
   - **Regra adicional desta passada**: um padrão presente apenas nos 2 projetos comerciais (2/2) **não** é promovido a "alta confiança geral" nem tratado como assinatura ampla — é marcado explicitamente como "observado em contexto comercial (amostra: 2/2 projetos comerciais), não extrapolar para residencial sem mais evidência" (ver `confidence_notes.commercial_sample_caution` no YAML). Padrões residenciais têm base de 6 projetos — mais robusta que a comercial, mas ainda abaixo do mínimo recomendado de 10-20.
5. Vários termos-chave foram reverificados com buscas diretas por documento (não apenas por agregação) especificamente para confirmar presença/ausência em cada um dos 2 documentos de cada projeto comercial, dado que esse é o eixo central desta rodada de curadoria.
6. Imagens (`pages/*.jpg`, `embedded-images/*`) não foram revisadas de forma exaustiva nesta passada — o escopo permanece majoritariamente textual.

## 2. Projetos-fonte e cobertura documental (categoria confirmada em catalog.json)

| # | client_project | Categoria (autoritativa) | Documentos | Páginas totais |
|---|---|---|---|---|
| 1 | ClinicaPatricia-2026 | **Comercial** (clínica estética) | 3: `comercial-clinicapatricia-2026-detalhamento-patricia-dias---compl` (63p), `comercial-clinicapatricia-2026-layout-a4-vistas` (106p), `comercial-clinicapatricia-2026-projeto-executivo-a3` (16p) | 185 |
| 2 | Tavora-2026 | **Comercial** (loja/joalheria) | 2: `comercial-tavora-2026-detalhamento-tavora-joias` (24p), `comercial-tavora-2026-projeto-executivo-távora-joias` (48p) | 72 |
| 3 | Clodoaldo-Vanusa-2025 | Residencial | 2: `residencial-clodoaldo-vanusa-2025-detalhamento-completo` (64p), `residencial-clodoaldo-vanusa-2025-executivo-completo` (91p) | 155 |
| 4 | Debora-Deivisson-2026 | Residencial | 2: `residencial-debora-deivisson-2026-detalhamento-dd` (36p), `residencial-debora-deivisson-2026-executivo-dd` (71p) | 107 |
| 5 | Gabi-2024 | Residencial (apto Evolution, Buritis/BH) | 3: `residencial-gabi-2024-detalhamento-final-ga` (81p), `residencial-gabi-2024-executivo-a3---geral` (18p), `residencial-gabi-2024-executivo-final-ga` (142p) | 241 |
| 6 | Patricia-Rafael-2025 | Residencial | 3: `residencial-patricia-rafael-2025-detalhamento` (40p), `residencial-patricia-rafael-2025-executivo-pr-a3` (23p), `residencial-patricia-rafael-2025-layout-pr` (101p) | 164 |
| 7 | Rafael-Mariana-2026 | Residencial (Apto R\|M, Jaraguá/BH) | 2: `residencial-rafael-mariana-2026-detalhamento-rm` (46p), `residencial-rafael-mariana-2026-rafael-e-mariana-executivo` (88p) | 134 |
| 8 | Sandra | Residencial (Casa S\|G, Cond. Estância do Lago) | 1: `residencial-sandra-sg-det-geral` (143p) | 143 |
| | **Total** | **6 residenciais + 2 comerciais** | **18 documentos** | **1.201 páginas** |

## 3. Padrões residenciais vs. comerciais — comparação direta

Esta seção resume o que mudou de granularidade em relação à v2, com a categoria agora confirmada em vez de inferida.

### 3.1 Padrões presentes em AMBOS os segmentos (alta confiança, robustos nos 2/2 comerciais)

Verificados diretamente documento a documento: MDF/Duratex, cuba, nicho, vidro, puxador Zen Design, porcelanato, painel ripado, tinta Suvinil, nota "CONFIRMAR MEDIDAS...", convenção de prancha (vista topo + vista A + vista B + perspectiva), grafia "PESPECTIVA", bloco de identificação padrão, dourado fosco, fita de LED, temperatura de cor 2700K/3000K, bancada+cuba, e — reclassificado nesta passada — **espelho** (ver seção 6).

### 3.2 Padrões EXCLUSIVOS do segmento residencial (0/2 nos projetos comerciais, verificado por busca direta com zero ocorrências)

Painel de TV, cabeceira, ilha de cozinha, closet, mesa de jantar, área gourmet, bege, trilho eletrificado (luminária), perfil de alumínio estrutural. Muitos desses são exclusivos por definição de programa (clínica e loja não têm "quarto", "sala de TV" ou "cozinha com ilha" no mesmo sentido de uma residência) — não é uma fraqueza do padrão, é um padrão condicionado ao tipo de ambiente.

### 3.3 Padrões observados nos 2/2 projetos comerciais mas com evidência residencial fraca ou distinta — NÃO generalizar

- **Fachada como prancha dedicada com índice e sequência de vistas** — 2/2 comercial, mas apenas 1/6 residencial (Patricia-Rafael-2025) com estrutura equivalente e completa; os outros 5 residenciais têm zero menções.
- **Estrutura completa do índice executivo por ambiente** ("PLANTA DE LAYOUT E TÉCNICA \<AMBIENTE\>" etc.) — evidência textual completa em apenas 1 dos 2 projetos comerciais (ClinicaPatricia-2026); não confirmada nem em Tavora-2026 nem em nenhum residencial.

### 3.4 Padrões assimétricos DENTRO do próprio segmento comercial (2 projetos, mas discordantes entre si)

- **Preto fosco**: presente em Tavora-2026, ausente em ClinicaPatricia-2026.
- **Mármore**: presente em ClinicaPatricia-2026, ausente em Tavora-2026.
- **Painel orgânico (nome literal)**: presente em ClinicaPatricia-2026, ausente em Tavora-2026.
- **Off-white**: presente em ClinicaPatricia-2026, ausente em Tavora-2026.

Isso reforça que "comercial" não é um bloco monolítico — com apenas 2 projetos, generalizações sobre "o que a arquiteta faz em projetos comerciais" são especialmente arriscadas.

## 4. Padrões condicionais

Ver `conditional_patterns` no `design-dna.yaml` (reescrito nesta passada). Resumo: room_patterns de programa residencial (sala de TV, quarto, ilha, jantar, closet) são condicionados à existência desses ambientes no programa — ausentes por definição nos 2 comerciais; documentação de fachada é condicionada a existir fachada no escopo do projeto (sempre nos 2 comerciais, só 1/6 nos residenciais); a convenção de prancha (vista topo/A/B/perspectiva) e as notas padronizadas de obra são universais, independentes de segmento.

## 5. Exceções e observações de cautela (herdadas e atualizadas da v2)

- **"Branco Gatinho efeito veludo"** e **efeito "veludo" (pintura) de forma geral** seguem como exceção clássica de preferência de 1 único client_project (ClinicaPatricia-2026). Verificação adicional nesta passada: as menções a "veludo" em Tavora-2026 (o outro projeto comercial) referem-se a TECIDO de estofado ("TECIDO VELUDO") e a joias em veludo, não a acabamento de pintura — portanto, mesmo dentro do comercial, o efeito veludo de pintura continua isolado a 1 projeto. Isso reforça, e não enfraquece, a conclusão da v2 de que é preferência pontual do cliente, não assinatura.
- **"Grafite"/"Chumbo"** e **marca de tinta "Coral"** seguem como preferências pontuais de 1 client_project cada (Gabi-2024 e ClinicaPatricia-2026, respectivamente).
- **"Painel orgânico" (produto nomeado)** — concentrado em 2 client_projects (1 comercial: ClinicaPatricia-2026; 1 residencial: Debora-Deivisson-2026); confirmado ausente no outro projeto comercial (Tavora-2026). O princípio formal mais amplo de curvas orgânicas é bem mais difundido (ambos os segmentos).
- **avoid_patterns não pôde ser preenchido** — mesma limitação da v2: o acervo registra decisões executadas, não recusadas.

## 6. Correções em relação à v2 (descobertas na reverificação direta desta passada)

Ao reler o acervo com o eixo residencial/comercial explícito, algumas atribuições específicas de projeto da v2 não se confirmaram em busca direta e foram corrigidas:

1. **Ilha de cozinha**: a v2 listava ClinicaPatricia-2026 entre os 6 projetos com "ilha". Busca direta nos 3 documentos de ClinicaPatricia-2026 e nos 2 de Tavora-2026 encontrou **zero** ocorrências do termo. O padrão é, portanto, exclusivo do residencial (5/6 projetos residenciais, não "6/8 incluindo 1 comercial").
2. **Trilho eletrificado**: a v2 atribuía este padrão também a ClinicaPatricia-2026. A única ocorrência de "TRILHO" nesse projeto é "EMBUTIR TRILHO DA PORTA RENTE AO PISO" — trilho de porta de correr (marcenaria/vidro), não luminária. O padrão de trilho eletrificado (luminária) é, portanto, exclusivamente residencial (2/6 projetos: Gabi-2024, Patricia-Rafael-2025), 0/2 comercial.
3. **Espelho**: a v2 classificava este padrão como "confiança média, 3/8 projetos" (ClinicaPatricia-2026, Rafael-Mariana-2026, Sandra). Busca direta encontrou o termo em pelo menos mais 4 documentos/projetos não contabilizados pela v2 (Clodoaldo-Vanusa-2025: 11 ocorrências; Gabi-2024: 24; Debora-Deivisson-2026: 2; Patricia-Rafael-2025: 15), além de confirmar Tavora-2026 (6 ocorrências). Reclassificado para alta confiança, ambos os segmentos — com a ressalva de que o texto não permite confirmar se é sempre espelho decorativo com moldura ou uso genérico do termo.
4. **Tinta Suvinil / Coral**: a v2 dava a entender que ClinicaPatricia-2026 usava Coral em vez de Suvinil. Busca direta mostra que ambas as marcas coexistem no mesmo projeto (Suvinil presente em todos os documentos de ClinicaPatricia-2026, Coral aparece adicionalmente). Suvinil confirmado em ambos os projetos comerciais — não é exclusividade residencial.
5. **Fachada residencial**: a v2 descrevia a evidência residencial como "uma citação isolada em Patricia-Rafael-2025". Busca direta mostra uma estrutura real (não isolada): índice "02. FACHADA", "Imagens Fachada" (3x), "Pespectiva - Fachada", "Planta Layout - Fachada" e uma sequência completa "Vista A/B/C/D - Fachada / Garagem", todos no mesmo `client_project`. Ainda é apenas 1/6 residenciais (evidência insuficiente para generalizar), mas a natureza da evidência é mais forte do que a v2 registrava.

Nenhuma dessas correções foi motivada pela mudança de categorização em si (a categoria de cada projeto já era conhecida na prática, mesmo que inferida) — elas emergiram da reverificação direta, documento a documento, motivada pelo maior rigor desta rodada em separar residencial de comercial termo a termo.

## 7. Itens de baixa confiança / pendências para a arquiteta revisar

Este é um **rascunho preliminar** (8 de 10-20 projetos recomendados; amostra comercial particularmente pequena, 2 projetos). Antes de aprovar o Design DNA (mudar `status` para `approved`), pedimos que a arquiteta confirme ou corrija:

1. **"Branco Gatinho efeito veludo"** e **"efeito veludo"** de pintura — preferência pessoal ainda sub-representada, ou escolha específica da Clínica Patrícia Dias?
2. **"Grafite"/"Chumbo"** (Gabi-2024) e **tinta Coral** (ClinicaPatricia-2026) — preferências pontuais de cliente ou padrões sub-representados?
3. **Metalon, perfil de alumínio estrutural, nogueira/freijó, trilho eletrificado** — todos em "confiança média", volume de citações baixo. Nenhum tem evidência no segmento comercial exceto metalon e nogueira/freijó (ambos só em ClinicaPatricia-2026, não em Tavora-2026).
4. **"Painel orgânico" (produto nomeado) vs. curvas orgânicas (princípio)** — confirmar se é nomenclatura padrão dela ou específica de 2 projetos (1 comercial, 1 residencial), já que nem o outro projeto comercial (Tavora-2026) usa o termo.
5. **Fachada** — perguntar diretamente: a arquiteta documenta fachada sistematicamente em projetos residenciais que são casas (não apartamentos)? A amostra atual (1/6 residenciais) é compatível com essa hipótese mas não a confirma.
6. **Área externa (jardim vs. gourmet)** — jardim aparece em 1/2 comercial + 3/6 residencial; gourmet é exclusivo residencial. Evidência ainda fraca para regras de composição.
7. **Estilização de renders (styling)** — tapete/almofada/vaso aparecem amplamente, mas sem cor/padronagem no texto. Requer revisão manual de imagens.
8. **Sustentabilidade** — nenhuma evidência textual encontrada. Campo deixado vazio propositalmente.
9. **`avoid_patterns` está vazio** — a arquiteta precisa listar explicitamente o que evita.
10. **Estrutura completa do índice de pranchas executivas** — evidência completa vem de um documento COMERCIAL (ClinicaPatricia-2026); confirmar se a mesma estrutura (incluindo bloco de fachada) é usada em cadernos residenciais, já que não foi possível confirmar isso textualmente em nenhum dos 6 projetos residenciais.
11. **Espelho** — reclassificado para alta confiança nesta passada; confirmar com a arquiteta se de fato é um elemento decorativo recorrente com intenção de composição, ou se o termo aparece em contextos variados (espelho de banheiro genérico, "acabamento espelhado" etc.) que inflaram a contagem.

Recomenda-se manter `status: in-review` até que a arquiteta valide os itens acima e, idealmente, até que o acervo cresça — sobretudo no segmento comercial, hoje com apenas 2 projetos-fonte.
