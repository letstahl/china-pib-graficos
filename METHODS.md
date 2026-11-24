# Métodos

## Gráfico 1: PIB nominal e PIB real da China, 2000–2025

- **Índice nominal.** PIB em dólares correntes de cada ano dividido pelo de 2000, vezes 100. Incorpora crescimento real, inflação e variação cambial.
- **Índice real.** Base 100 em 2000, encadeado pela taxa de crescimento real anual do FMI:

  `real(2000) = 100;  real(t) = real(t−1) × (1 + NGDP_RPCH(t) / 100)`

  Mede apenas a variação do volume produzido.
- **Área amarela.** A diferença entre as curvas corresponde a inflação e variação cambial do yuan frente ao dólar.
- **Médias do painel de baixo.** Média simples das taxas anuais de 2001 a 2010, de 2011 a 2019 e de 2020 a 2025.
- **Resultado.** Nominal ×16,0, real ×6,9, e médias de 10,6%, 7,4% e 4,9% ao ano.

## Gráfico 2: China como % dos EUA, em quatro medidas

Para cada ano, `100 × China / EUA` para (1) PIB total em PPC (`PPPSH`), (2) PIB total em US$ correntes (`NGDPD`), (3) PIB per capita em PPC (`PPPPC`) e (4) PIB per capita em US$ correntes (`NGDPDPC`).
Para o `PPPSH`, a razão entre as participações no PIB mundial equivale à razão entre os PIBs em PPC, pois o denominador (PIB mundial) é o mesmo.

## Gráfico 3: convergência a partir de 20% da renda per capita dos EUA

Para cada país, `100 × PIB per capita do país / PIB per capita dos EUA` no mesmo ano (Maddison). O ano zero é o primeiro ano com razão ≥ 20%: Japão em 1950, Taiwan em 1973, Coreia do Sul em 1979 e China em 2011. São exibidos os 30 anos seguintes a cada ano zero.

## Gráfico 4: comércio com a China e com os EUA

Séries do Lowy Institute sem transformação, de 2001 (entrada da China na OMC) a 2023.

## Conferência dos números

`python src/make_figures.py` imprime os valores principais. Valores esperados:

```
G1  PIB nominal x16.0 | PIB real x6.9 | 2001-2010: 10.6% | 2011-2019: 7.4% | 2020-2025: 4.9%
G2  2025, % dos EUA: tot_ppc 133.7 | tot_usd 63.6 | pc_ppc 32.5 | pc_usd 15.5
G3  ano em que cada país atinge 20%: JPN 1950 | KOR 1979 | TWN 1973 | CHN 2011
G4  2023: 145 economias comerciam mais com a China; 112 com o dobro ou mais
```

## Limitações

- Os dados em dólares correntes dependem do câmbio de cada ano, portanto a comparação em US$ é sensível a ele.
- A PPC provém de pesquisas de preços (ICP), revisadas periodicamente. Os níveis variam entre edições do WEO.
- Maddison e FMI têm metodologias e anos-base distintos; não são combinados no mesmo gráfico.
- O Gráfico 4 usa as séries do Figure 1 do Lowy, calculadas pelo Lowy a partir de dados do FMI. Não são dados brutos de comércio.
- O valor de 2025 é estimativa do FMI.
