# Dados

Os arquivos de `data/raw/` são cópias dos dados das fontes, sem transformação (CSV, UTF-8, ponto como separador decimal). Os valores calculados (índices, razões, anos de partida) ficam em `data/processed/`, gerados por `src/make_figures.py`. Os arquivos de `raw/` não são editados manualmente.

## Origem e conferência

Os dados foram copiados manualmente das fontes entre 14 e 16 nov. 2026. Os comandos dessa coleta não foram registrados, portanto não há script de download.
Em **23 nov. 2026** cada arquivo foi conferido contra o site de origem, por comparação programática no navegador (duas rodadas no mesmo dia, com o mesmo resultado).

| arquivo | endereço consultado | resultado |
|---|---|---|
| `imf_weo_2026oct.csv` | API do DataMapper: `https://www.imf.org/external/datamapper/api/v1/NGDPD` (idem para `NGDPDPC`, `PPPSH`, `PPPPC` e `NGDP_RPCH`, trocando o código no final da URL) | 333 valores (9 séries, 1990–2026), nenhuma divergência. Diferença relativa máxima de 0,005%, por arredondamento do CSV. |
| `maddison_gdppc.csv` | CSV do Our World in Data: `https://ourworldindata.org/grapher/gdp-per-capita-maddison-project-database.csv?csvType=full&useColumnShortNames=false` | 5 países × 73 anos (1950–2022). Contagem, soma e soma ponderada por ano **idênticas**. |
| `lowy_trade.csv` | dados do Figure 1 dentro do código da página do Lowy (arquivo `/_app/immutable/chunks/figure-1.<hash>.js`, e o hash varia entre versões) | 2 séries × 24 anos (2000–2023), **idênticas**. |

### Como acessar cada fonte

**FMI (WEO).** Página: https://www.imf.org/external/datamapper/NGDPD@WEO (substituir `NGDPD` pelo código do indicador).
Dados em JSON: https://www.imf.org/external/datamapper/api/v1/NGDPD (idem para `NGDPDPC`, `PPPSH`, `PPPPC` e `NGDP_RPCH`; significado de cada código na tabela de `raw/imf_weo_2026oct.csv`, abaixo). Estrutura da resposta: `values → indicador → país (ISO-3) → ano`. A conferência compara `CHN` e `USA` com o CSV.
A API retorna sempre a edição mais recente do WEO; os valores mudam quando uma nova edição é publicada.

**Maddison, via Our World in Data.** Página: https://ourworldindata.org/grapher/gdp-per-capita-maddison-project-database. O CSV completo está na aba *Download* (ou no endereço da tabela acima). Colunas: `Entity`, `Code`, `Year` e `GDP per capita`. Filtro: `CHN`, `JPN`, `KOR`, `TWN` e `USA`, 1950 a 2022.

**Lowy Institute.** Página: https://interactives.lowyinstitute.org/features/china-versus-america-on-global-trade/. Os dados são os do **Figure 1** ("Number of economies that trade more with China than with the United States"). A página não oferece download; os pontos estão no código carregado por ela.
1. Abrir a página, pressionar F12 e acessar a aba *Network*.
2. Limpar o campo de filtro e selecionar o tipo **JS** (*Fetch/XHR* não lista o arquivo, que é um script).
3. Recarregar a página (Ctrl+R) com o painel aberto; requisições anteriores à abertura do painel não aparecem.
4. Filtrar por `figure-1`, selecionar `figure-1.<hash>.js` e abrir a aba *Response*, que lista os pontos `{x: ano, y: valor}` das duas séries.

Alternativa: ler os valores de cada ano no *tooltip* do gráfico. O texto da página também confirma os valores principais: 145 economias em 2023 (de 205), 112 com o dobro ou mais, e 139 e 92 em 2018.

### Procedimento da conferência de 23 nov. 2026

Executada no navegador. Para cada fonte: acesso ao endereço, listagem das requisições da página (no Lowy, identificação do arquivo `figure-1.<hash>.js`), obtenção dos dados pelo console da própria página e comparação com os CSVs de `raw/`. Critério: tolerância de 0,06% no FMI (CSV arredondado em cerca de 5 algarismos) e igualdade exata no Maddison e no Lowy.

## `raw/imf_weo_2026oct.csv`

| coluna | o que é |
|---|---|
| `indicator` | código do indicador (tabela abaixo) |
| `country` | código ISO 3166-1 alfa-3 (`CHN` ou `USA`) |
| `year` | de 1990 a 2026 |
| `value` | valor na unidade do indicador |
| `is_projection` | 1 se `year` = 2026 (projeção do FMI), 0 nos outros anos |

| `indicator` | série do WEO | unidade | usado em |
|---|---|---|---|
| `NGDPD` | PIB nominal, dólares correntes | US$ bilhões | Gráficos 1 e 2 |
| `NGDPDPC` | PIB per capita, dólares correntes | US$ | Gráfico 2 |
| `PPPSH` | participação no PIB mundial em PPC | % | Gráfico 2 |
| `PPPPC` | PIB per capita em PPC, dólares internacionais correntes | US$ internacionais | Gráfico 2 |
| `NGDP_RPCH` | crescimento real do PIB (só `CHN`) | % ao ano | Gráfico 1 |

- **Fonte:** FMI, *World Economic Outlook*, outubro de 2026, via DataMapper. https://www.imf.org/external/datamapper
- **Acesso:** 14 nov. 2026, conferido em 23 nov. 2026.
- **Observação:** o FMI trata 2025 como estimativa. 2026 é projeção e **nenhum gráfico usa** esse ano.
- **Atribuição (termos do FMI para dados estatísticos):** Source: International Monetary Fund, World Economic Outlook Database, October 2026, https://www.imf.org/external/datamapper/NGDPD@WEO
- **Termos:** os dados do FMI podem ser copiados e redistribuídos com atribuição, sem alterar sua natureza ou exatidão. `raw/` contém cópias sem alteração; as transformações estão em `METHODS.md`. Termos completos: https://www.imf.org/en/about/copyright-and-terms. Os dados não implicam endosso do FMI.

## `raw/maddison_gdppc.csv`

| coluna | o que é |
|---|---|
| `country` | `CHN`, `JPN`, `KOR`, `TWN` ou `USA` |
| `year` | de 1950 a 2022 |
| `gdppc_2011_intl_usd` | PIB per capita em dólares internacionais de 2011 |

- **Fonte:** Bolt, J.; van Zanden, J. L. Maddison Project Database, versão 2023. Groningen Growth and Development Centre, 2024. Obtida pelo Our World in Data.
- **Licença da fonte:** CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). Atribuição: Bolt e van Zanden, Maddison Project Database 2023.
- **Observação:** é uma série histórica de longo prazo do PIB per capita em PPC. Os níveis **não são comparáveis** com o `PPPPC` do FMI (ano-base de preços e metodologia distintos). Por isso o Gráfico 3 usa apenas o Maddison e o Gráfico 2 apenas o FMI.

## `raw/lowy_trade.csv`

| coluna | o que é |
|---|---|
| `year` | de 2000 a 2023 |
| `economies_trading_more_with_china` | número de economias que comerciam mais bens com a China do que com os EUA |
| `economies_trading_twice_or_more_with_china` | número de economias cujo comércio com a China é o dobro ou mais do que com os EUA |

- **Fonte:** Lowy Institute, *China versus America on global trade*, 2025. https://interactives.lowyinstitute.org/features/china-versus-america-on-global-trade/
- **Acesso:** 16 nov. 2026, conferido em 23 nov. 2026.
- **Observação:** os valores são idênticos aos do Figure 1 da página, calculado pelo Lowy sobre o *Direction of Trade Statistics* do FMI. Em 2023, 145 de 205 economias comerciavam mais com a China.
- **Termos:** conferir com o Lowy Institute antes de redistribuir. Havendo restrição, o arquivo deve ser removido e mantida apenas a referência.

## `processed/`

| arquivo | gráfico | o que tem |
|---|---|---|
| `fig1_china_gdp_index.csv` | 1 | PIB nominal (US$ bi), índice nominal e índice real encadeado (2000 = 100), crescimento real |
| `fig2_china_vs_usa.csv` | 2 | PIB total e per capita da China como % dos EUA, em PPC e em US$ |
| `fig3_catchup_from_20pct.csv` | 3 | PIB per capita em PPC como % dos EUA, a partir do ano em que cada país chega a 20% |
