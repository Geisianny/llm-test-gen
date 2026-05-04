# Investigando o uso de LLM para geração de cenários Gherkin

Resumo:

<p align="justify">
A crescente demanda por qualidade em software tem impulsionado
práticas como Behavior-Driven Development (BDD) e testes de aceitação automatizados, nos quais cenários em Gherkin descrevem
o comportamento esperado do sistema. No entanto, a elaboração
manual de cenários é trabalhosa e sujeita à inconsistências. Neste
contexto, realizamos um estudo empírico para avaliar a viabilidade
do uso do modelo LLaMA-4 Maverick 17B-128E na geração de
cenários Gherkin a partir de histórias de usuário. Partindo de uma
amostra de 104 histórias de 26 projetos do GitHub, geramos 520 cenários utilizando few-shot prompting e avaliamos sua qualidade. Os
resultados revelaram ausência de erros sintáticos e boa aderência às
boas práticas (apenas 4 cenários com defeito, excluindo-se erros de
indentação e comprimento excessivo de step ou título, reparáveis
por simples ajuste no prompt). A similaridade textual com cenários
humanos, medida por TF-IDF e embeddings, apresentou valores intermediários (0,44 e 0,58), sugerindo que o modelo capturou melhor
o comportamento funcional dos cenários sem reproduzir exatamente o estilod de escrita humana. No entanto, a inspeção manual
dos casos extremos sinalizou a avaliação de similaridade textual
foi, em geral, pouco conclusiva quanto à adequação do vocabulário
adotado nos cenários gerados, em partes devido à baixa qualidade
de parte dos cenários de referência. No mais, constatamos alta cobertura funcional dos cenários gerados a partir da avaliação manual
destes, o que significa que os cenários cobriram satisfatoriamente
o fluxo principal e os fluxos alternativos esperados para a história,
conforme instruído pelo prompt. Por fim, a partir da análise manual
de uma subamostra de 104 cenários (1 cenário por história) por dois
revisores (com taxa de concordância de 87,5%), constatamos alta
coesão semântica dos cenários gerados, ou seja, os cenários se mostraram alinhados aos requisitos de software subjacentes às histórias.
Em conjunto, os achados sugerem que o modelo é viável como suporte inicial à geração de cenários Gherkin, contribuindo para a
automação e padronização dos testes de aceitação, sem dispensar a
validação humana.

</p>

---

## Configuração de estudo

- [Script de busca no github](./0-GitHubSearch)
- [Script de dowloader dos dados](./1-downloader)
- [Script de filtragem e seleção dos dados](./2-PaserAndFiltering)
- [Script de seleção da amostra](./2.1-RandomSelection)
- [Script de busca de informações dos repositorios](./3-Characterization)
- [Script de geração dos cenarios](./5-LlmUsToTest)
- [Script para execução das metricas](./6-FeatureEvaluation)
- [Script para execução das metricas de similaridade](./7-scenario_quality)
- [Dados coletados](./featuresEvaluationSummary)

---

## Resultados da avaliação

- [Informações sobre os repositorios da amostra](./repositorios_amostra/)
- [PP1: Com que frequência os cenários gerados por LLM são sintaticamente corretos e seguem as boas práticas?]()
- [PP2: Em que medida os cenários gerados por LLM são textualmente similares aos gerados por humanos?]()
- [PP3: Com que frequência os cenários gerados apresentam coesão semântica em relação às histórias de usuário?]()
- [PP4: Com que frequência os cenários gerados apresentam cobertura funcional adequada das histórias de usuário?]()
- [Outras informações](./outras_informacoes)

