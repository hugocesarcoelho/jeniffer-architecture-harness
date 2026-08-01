# Evidence Report — Design DNA (Jeniffer Melo Arquitetura)

Data: 2026-08-01
Status do Design DNA associado: `in-review` (rascunho preliminar, pendente de validação da arquiteta)

## 1. Metodologia

1. Fonte: `docs/knowledge-base/extracted/`, contendo 18 documentos técnicos (`document.txt` extraído de PDF + imagens de página) provenientes de 8 pastas de cliente (`client_project`) distintas, listadas em `docs/knowledge-base/extracted/catalog.json`.
2. Para cada termo de material/cor/iluminação/marcenaria/composição candidato a padrão, foi feita busca (`grep`) em todos os 18 `document.txt` e contado: (a) número total de ocorrências, (b) número de documentos com pelo menos 1 ocorrência, (c) número de **`client_project` distintos** com pelo menos 1 ocorrência.
3. Regra de confiança aplicada (conforme instrução da tarefa):
   - **Alta confiança**: padrão presente em ≥ 3 `client_project` distintos.
   - **Confiança média**: padrão presente em exatamente 2 `client_project` distintos.
   - **Evidência insuficiente / preferência do cliente**: padrão presente em apenas 1 `client_project`. Esses casos foram deliberadamente mantidos fora de `signature_patterns`/`principles` como regra geral e documentados em `confidence_notes.insufficient_evidence`.
4. Padrões de documentação (estrutura de prancha, nomenclatura, notas padrão) foram identificados por leitura direta de trechos de `document.txt` (blocos de identificação, sequência de páginas, notas repetidas) e confirmados por busca de recorrência entre projetos.
5. Imagens (`pages/*.jpg`, `embedded-images/*`) não foram revisadas de forma exaustiva nesta passada — o escopo desta análise foi majoritariamente textual, conforme orientação da tarefa. Onde a evidência textual foi insuficiente para caracterizar estilização visual (cor de tapete, padronagem etc.), isso foi registrado como pendência em `confidence_notes.insufficient_evidence`.

### Aviso importante sobre o tamanho da amostra

Esta base tem **apenas 8 projetos-fonte** (18 documentos, ~1.201 páginas). O guia de curadoria do acervo recomenda 10-20 projetos como base representativa mínima. Portanto, **todo o Design DNA gerado a partir desta rodada é preliminar/rascunho**, não uma conclusão definitiva. Padrões classificados aqui como "alta confiança" o são apenas em relação ao critério interno de recorrência entre ≥3 dos 8 projetos disponíveis — e podem mudar de classificação (ou ser refutados) à medida que mais projetos forem ingeridos e a arquiteta revisar o conteúdo.

## 2. Projetos-fonte e cobertura documental

| # | client_project | Tipo (inferido) | Documentos | Páginas totais |
|---|---|---|---|---|
| 1 | ClinicaPatricia-2026 | Comercial (clínica estética) | 3: `clinicapatricia-2026-detalhamento-patricia-dias---compl` (63p), `clinicapatricia-2026-layout-a4-vistas` (106p), `clinicapatricia-2026-projeto-executivo-a3` (16p) | 185 |
| 2 | Clodoaldo-Vanusa-2025 | Residencial | 2: `clodoaldo-vanusa-2025-detalhamento-completo` (64p), `clodoaldo-vanusa-2025-executivo-completo` (91p) | 155 |
| 3 | Debora-Deivisson-2026 | Residencial | 2: `debora-deivisson-2026-detalhamento-dd` (36p), `debora-deivisson-2026-executivo-dd` (71p) | 107 |
| 4 | Gabi-2024 | Residencial (apto Evolution, Buritis/BH) | 3: `gabi-2024-detalhamento-final-ga` (81p), `gabi-2024-executivo-a3---geral` (18p), `gabi-2024-executivo-final-ga` (142p) | 241 |
| 5 | Patricia-Rafael-2025 | Residencial | 3: `patricia-rafael-2025-detalhamento` (40p), `patricia-rafael-2025-executivo-pr-a3` (23p), `patricia-rafael-2025-layout-pr` (101p) | 164 |
| 6 | Rafael-Mariana-2026 | Residencial (Apto R\|M, Jaraguá/BH) | 2: `rafael-mariana-2026-detalhamento-rm` (46p), `rafael-mariana-2026-rafael-e-mariana-executivo` (88p) | 134 |
| 7 | Sandra | Residencial (Casa S\|G, Cond. Estância do Lago) | 1: `sandra-sg-det-geral` (143p) | 143 |
| 8 | Tavora-2026 | Comercial (loja/joalheria) | 2: `tavora-2026-detalhamento-tavora-joias` (24p), `tavora-2026-projeto-executivo-távora-joias` (48p) | 72 |
| | **Total** | | **18 documentos** | **1.201 páginas** |

Observação de escopo: 6 dos 8 projetos são residenciais e 2 são comerciais (clínica e loja). Padrões observados apenas em ClinicaPatricia-2026 e/ou Tavora-2026 (ex.: fachada) podem refletir convenções de projeto comercial e foram sinalizados como tal, não generalizados para residências.

## 3. Padrões recorrentes (alta confiança — ≥3 projetos distintos)

Cada item abaixo cita o(s) `document_id` mais representativos como evidência (lista completa de projetos no `design-dna.yaml`).

- **MDF (marca Duratex) como substrato dominante de marcenaria** — 1.940 ocorrências de "MDF" em 17/18 documentos, 8/8 projetos; "DURATEX" citado nominalmente em 575 ocorrências, 9 documentos, 8/8 projetos. Evidência: `gabi-2024-detalhamento-final-ga` (pág. 2, "APARADOR EM MDF BRANCO DIAMANTE - DURATEX"); `rafael-mariana-2026-detalhamento-rm` (pág. 3, "MDF CARVALHO HANOVER - DURATEX", "MDF CINZA FÓSSIL - DURATEX").
- **Fita de LED embutida contínua** — 328 ocorrências, 18/18 documentos, 8/8 projetos. Evidência: `rafael-mariana-2026-detalhamento-rm` (pág. 3, "COM CAVA LATERAL PARA FITA DE LED EMBUTIDA (NÃO DEIXAR LED APARENTE)").
- **Temperatura de cor especificada (2700K/3000K)** — 144-149 ocorrências, 16/18 documentos, 8/8 projetos. Evidência: `rafael-mariana-2026-detalhamento-rm` (pág. 3, "FITA DE LED 2700K").
- **Nichos embutidos em marcenaria/gesso** — 185 ocorrências, 14/18 documentos, 8/8 projetos.
- **Bancada com cuba (mármore/pedra)** — "BANCADA": 237 ocorrências/18 documentos/8 projetos; "CUBA": 103 ocorrências/17 documentos/8 projetos; "MÁRMORE": 67 ocorrências/11 documentos/7 projetos (falta apenas Tavora-2026).
- **Porcelanato em pisos/revestimentos** — 124 ocorrências, 14 documentos, 7/8 projetos (falta apenas Rafael-Mariana-2026).
- **Vidro (boxes, guarda-corpos, tampos)** — 262 ocorrências, 17 documentos, 8/8 projetos.
- **Painel ripado como revestimento** — 145 ocorrências, 14 documentos, 7/8 projetos (falta apenas Rafael-Mariana-2026). Evidência: `gabi-2024-detalhamento-final-ga` (pág. 2, rótulo "Ripado" em detalhe de aparador).
- **Puxador com marca/acabamento definidos, majoritariamente Zen Design** — "PUXADOR": 576 ocorrências/15 documentos/8 projetos; marca "ZEN DESIGN": 106 ocorrências/8 documentos/7 projetos (falta apenas Debora-Deivisson-2026). Evidência: `gabi-2024-detalhamento-final-ga` (pág. 2, "PUXADOR PLYMOUTH DOURADO- ZEN DESING").
- **Dourado / dourado fosco como metal de assinatura** — "DOURADO": 481 ocorrências/17 documentos/8 projetos; "DOURADO FOSCO": 117 ocorrências/11 documentos/6 projetos.
- **Preto / preto fosco como cor de contraste** — "PRETO": 426 ocorrências/17 documentos/7-8 projetos; "PRETO FOSCO": 137 ocorrências/12 documentos/6 projetos.
- **Branco/off-white como base cromática** — "BRANCO": 686 ocorrências/18 documentos/8 projetos; "OFF WHITE": 107 ocorrências/7 documentos/5 projetos.
- **Rebaixo de forro em gesso** — 173 ocorrências, 13 documentos, 8/8 projetos.
- **Painel de TV como peça central de sala** — 46 ocorrências, 10 documentos, 6/8 projetos.
- **Ilha de cozinha** — 42 ocorrências, 11 documentos, 6/8 projetos.
- **Cabeceira como peça central de quarto** — 187 ocorrências, 11 documentos, 6/8 projetos.
- **Tinta Suvinil especificada nominalmente** — 159 ocorrências, 11 documentos, 7/8 projetos.
- **Bloco de identificação de prancha padronizado** ("Jeniffer Melo Arquitetura", telefone, e-mail, CAU A186976-0, campos PROJETO/DATA/FOLHA/CLIENTE/DESENHO/ARQUITETA) — 1.188 ocorrências, 18/18 documentos, 8/8 projetos.
- **Grafia "PESPECTIVA" (sem "r") em vez de "PERSPECTIVA"** — 392 ocorrências, 14 documentos, 8/8 projetos. Este é um hábito de nomenclatura pessoal muito consistente e um bom identificador de autenticidade de documento. Evidência: `rafael-mariana-2026-detalhamento-rm` (pág. 2, campo DESENHO = "Pespectiva").
- **Convenção de prancha (vista topo + vista A + vista B + perspectiva, cada uma com escala própria)** — "VISTA TOPO": 426 ocorrências, 8 documentos de detalhamento, 8/8 projetos. Evidência: `rafael-mariana-2026-detalhamento-rm` (pág. 3).
- **Nota "CONFIRMAR MEDIDAS NO LOCAL ANTES DA EXECUÇÃO"** — 103 ocorrências, 10 documentos, 7/8 projetos.
- **Callout de material no padrão "\<PEÇA\> EM/NO \<MATERIAL\> \<COR\> - \<MARCA\>"** — confirmado consistentemente em amostras de todos os projetos revisados em detalhe.

## 4. Padrões condicionais

- Quando o ambiente é **sala de estar/TV** → painel de marcenaria com nicho para TV + fita de LED perimetral (6/8 projetos).
- Quando o ambiente é **banheiro, lavabo ou cozinha** → bancada em mármore/pedra com cuba de apoio ou esculpida (7-8/8 projetos).
- Quando há **espelho decorativo** em áreas sociais/banheiros → tende a vir emoldurado por perfil metálico dourado fosco ou preto fosco (evidenciado em ClinicaPatricia-2026, Rafael-Mariana-2026 e Sandra — 3/8 projetos).
- Quando o projeto é **comercial** (ClinicaPatricia-2026, Tavora-2026) → a documentação inclui prancha dedicada de fachada e índice de pranchas por ambiente no formato "PLANTA DE LAYOUT E TÉCNICA \<AMBIENTE\>" + "VISTAS \<AMBIENTE\>" (evidência textual completa em `clinicapatricia-2026-layout-a4-vistas`, páginas 1-2). Essa estrutura não deve ser presumida para fachada residencial, sem evidência equivalente no acervo atual.
- Quando a prancha é de **detalhamento de marcenaria** → segue sempre a convenção fixa vista topo/vista A/vista B/perspectiva + nota de confirmação de medidas em obra (8/8 projetos).

## 5. Exceções e observações de cautela

- **"Branco Gatinho efeito veludo"** — este é exatamente o tipo de callout citado como exemplo na tarefa, e a análise confirma que ele é uma **exceção clássica de confusão cliente-vs-arquiteta**: aparece 88 vezes, mas só em documentos de **1 único client_project** (ClinicaPatricia-2026: `clinicapatricia-2026-detalhamento-patricia-dias---compl`, páginas 4-6; `clinicapatricia-2026-layout-a4-vistas`, páginas 4 e 22). Foi mantido fora de `signature_patterns.colors` e registrado em `insufficient_evidence`.
- **Efeito "veludo" (VELVET) de pintura** — 84 ocorrências, mas 83 delas concentradas em ClinicaPatricia-2026; a única outra menção (`patricia-rafael-2025-layout-pr`, 1 ocorrência) é fraca demais para confirmar um padrão de 2 projetos com robustez. Tratado como preferência de cliente.
- **"Grafite"/"Chumbo" como cor de marcenaria** — só em Gabi-2024. Preferência pontual do cliente, não da arquiteta.
- **Marca de tinta "Coral"** — só em ClinicaPatricia-2026 (a arquiteta usa predominantemente Suvinil nos demais projetos). Possível decisão específica de cliente ou de fornecedor local desse projeto.
- **"Painel orgânico" como nome literal de produto** (vs. o princípio mais amplo de curva/forma orgânica) — a frase exata "PAINEL ORGÂNICO" está concentrada em apenas 2 projetos (ClinicaPatricia-2026 e Debora-Deivisson-2026, 38 ocorrências), enquanto o termo mais genérico "orgânico/orgânica" (que inclui curvas, formatos, sancas orgânicas etc.) aparece em 6-8 projetos. Isso sugere que o **princípio formal** (curvas orgânicas) é da arquiteta, mas o **nome de produto específico** "painel orgânico em gesso" pode ser mais um vocabulário adotado nesses 2 projetos — vale confirmar com a arquiteta se ela usa esse nome sistematicamente ou não.
- **Estrutura completa do índice executivo** ("PLANTA DE DEMOLIÇÃO E CONSTRUÇÃO", "PLANTA DE PONTOS HIDRÁULICOS" etc.) — evidência textual completa apenas em ClinicaPatricia-2026; embora nomenclaturas parecidas apareçam em Gabi-2024, Patricia-Rafael-2025 e Rafael-Mariana-2026, não há garantia de que a sequência completa seja idêntica nesses projetos (pode ser limitação de extração de texto do índice, não ausência real do padrão).
- **avoid_patterns não pôde ser preenchido**: os documentos registram apenas decisões executadas. As únicas ocorrências do termo "evitar" encontradas no corpus referem-se a coordenação técnica de obra (ex.: "A EXECUÇÃO DO FORRO DEVE SER REALIZADA CONJUNTAMENTE COM A PLANTA DE ILUMINAÇÃO PARA EVITAR INCOMPATIBILIDADES ENTRE PONTOS DE LUZ E RECORTES NO GESSO" — `clinicapatricia-2026-projeto-executivo-a3`, ~linha 561; "PINGADEIRA METÁLICA NAS BORDAS DO VIDRO PARA EVITAR RETORNO DA ÁGUA" — `patricia-rafael-2025-detalhamento`, ~linha 2560), não a preferências estéticas evitadas. Isso ficou registrado como pendência explícita para a arquiteta.

## 6. Itens de baixa confiança / pendências para a arquiteta revisar

Este é um **rascunho preliminar** (8 de 10-20 projetos recomendados). Antes de aprovar o Design DNA (mudar `status` para `approved`), pedimos que a arquiteta confirme ou corrija:

1. **"Branco Gatinho efeito veludo"** e **"efeito veludo"** de pintura em geral — é uma cor/acabamento de assinatura pessoal que simplesmente ainda não apareceu em outros projetos do acervo, ou foi uma escolha específica para o conceito da Clínica Patrícia Dias?
2. **"Grafite"/"Chumbo"** (Gabi-2024) e **tinta Coral** (ClinicaPatricia-2026) — preferências pontuais de cliente ou possíveis padrões da arquiteta ainda sub-representados na amostra?
3. **Metalon/perfil tubular metálico**, **espelho decorativo com moldura metálica**, **trilho eletrificado**, **perfil de alumínio estrutural** e **nogueira/freijó** — todos atingem o piso técnico de "alta confiança" (≥3 projetos) mas com volume de citações baixo (7 a 25 ocorrências). Recomenda-se tratá-los como "média confiança" na prática até serem reforçados por mais projetos.
4. **"Painel orgânico" (produto nomeado) vs. curvas orgânicas (princípio)** — pedir à arquiteta para confirmar se "painel orgânico em gesso" é nomenclatura padrão dela ou específica de 2 projetos.
5. **Fachada residencial** — não há evidência no acervo atual (só fachada comercial, em 2 projetos). Nenhuma regra foi criada para `room_patterns.fachada` além do alerta.
6. **Área externa** — evidência fraca e genérica (4/8 projetos, sem detalhamento). Precisa de mais amostra para virar padrão.
7. **Estilização de renders (styling)** — tapete/almofada/vaso aparecem em 7/8 projetos, mas o texto extraído não permite caracterizar cor, padronagem ou composição desses itens. Requer revisão manual das imagens de página (`pages/*.jpg`) pela arquiteta, ou um passe de visão computacional dedicado, fora do escopo desta análise textual.
8. **Sustentabilidade** — nenhuma evidência textual encontrada (materiais certificados, reaproveitamento etc.). Campo deixado vazio propositalmente.
9. **`avoid_patterns` está vazio** — a arquiteta precisa listar explicitamente materiais/cores/composições que evita, pois isso não é dedutível de projetos executados.
10. **Estrutura completa do índice de pranchas executivas** — confirmar se a sequência vista em ClinicaPatricia-2026 (perspectiva → demolição/construção → piso/acabamentos → hidráulica → elétrica → forro → iluminação → imagens → por ambiente → fachada → notas) é de fato o padrão universal dela, mesmo quando não capturado integralmente em texto nos outros projetos.

Recomenda-se manter `status: in-review` até que a arquiteta valide os itens acima e, idealmente, até que o acervo cresça para 10-20 projetos-fonte.
