# FutBI

FutBI e uma base analitica para futebol pensada para transformar dados brutos de partidas em informacao pronta para decisao.

Com pipeline simples e direta, o projeto converte arquivos JSON de eventos, escalacoes e jogos em dados estruturados no MySQL, acelerando analises tecnicas, taticas e de performance.

## Por que FutBI

- Centraliza dados de jogo em um modelo unico e consultavel.
- Reduz tempo entre coleta de dados e insight.
- Facilita evolucao de dashboards, relatorios e modelos analiticos.
- Organiza ingestao e transformacao em fluxo claro por dominio.

## O que o projeto entrega

- Ingestao de partidas (`matches`) com informacoes principais do confronto.
- Ingestao de escalacoes (`lineups`) para leitura de elenco e contexto.
- Ingestao de eventos (`events`) para analise de acao a acao.
- Base pronta para exploracao em BI, ciencia de dados e scouting.

## Publico-alvo

- Analistas de desempenho
- Times de dados em clubes e empresas esportivas
- Profissionais de BI esportivo
- Pesquisadores e estudantes de analytics no futebol

## Estrutura do projeto

- `conexao.py`: camada de conexao com banco e execucao de queries.
- `data/raw/`: dados brutos em JSON (`events`, `lineups`, `matches`).
- `src/ingest/`: notebooks de carga por entidade.
- `src/transform/`: notebooks de transformacao e analise.

## Requisitos tecnicos

- Python 3.10+
- MySQL
- Dependencias principais: `mysql-connector-python`, `python-dotenv`, `jupyter`, `pandas`


## Inicio rapido

1. Configure as variaveis de ambiente no arquivo `.env`.
2. Abra os notebooks de ingestao em `src/ingest/`.
3. Execute as celulas na ordem para carregar dados no banco.

Exemplos de notebooks:

- `src/ingest/matchesLoad.ipynb`
- `src/ingest/eventsLoad.ipynb`
- `src/ingest/lineupLoad.ipynb`

## Visao de evolucao

FutBI foi estruturado para crescer por etapas: primeiro a consolidacao da base historica, depois a camada de metricas e, por fim, produtos analiticos de maior valor como deteccao de padroes taticos, comparacao de atletas e apoio a tomada de decisao em tempo proximo ao real.
