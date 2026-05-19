# Faria Lima Simulator 📈

**Disciplina:** Introdução à Programação | 1º Período — Engenharia de Computação  
**Integrantes:** Felipe Allan Nascimento Cruz & Nickollas Teixeira  
**Status do Projeto:** Entrega 2 (Versão Inicial do Algoritmo)

---

## 📝 Sobre o Projeto
O **Faria Lima Simulator** é um simulador financeiro textual baseado em terminal. O usuário assume o papel de um investidor iniciante que gerencia uma carteira composta por 5 ações de grande relevância no mercado (`NVIDIA`, `AAPL`, `MSFT`, `PETR4`, `VALE3`) ao longo de um ciclo fechado de 12 meses. O objetivo principal é reagir estrategicamente às notícias mensais e acumular patrimônio.

### 🎯 Regras de Negócio Globais
* **Capital Inicial:** R$ 10.000,00 de saldo disponível em conta no Mês 1.
* **Aporte Mensal (Salário):** Todo início de mês (a partir do Mês 2), o saldo do jogador recebe um acréscimo automático de **R$ 1.000,00**.
* **Condição de Vitória:** Terminar o Mês 12 com um **Patrimônio Total igual ou superior a R$ 25.000,00**.
* **Condição de Derrota:** Terminar o Mês 12 com um patrimônio inferior a R$ 25.000,00 ou atingir a insolvência (saldo negativo).

---

## 🏗️ Arquitetura Modular de Software (5 Arquivos)

Para cumprir rigorosamente as diretrizes de organização e evitar o uso de variáveis globais, o sistema gerencia todo o seu fluxo por meio de um único dicionário centralizado chamado `estado`. As funções dos arquivos dos integrantes recebem esse dicionário por parâmetro, processam as alterações e o retornam atualizado para o arquivo principal.

### 🗂️ Divisão de Responsabilidades

1. **`main.py` (O Maestro):**
   * Contem a estrutura inicial do dicionário `estado`.
   * Executa o loop principal `while not verificar_vitoria_derrota(estado):`.
   * Não possui lógica matemática ou prints diretos; apenas orquestra a chamada de funções externas.

2. **`felipe_visual.py` (Interface de Usuário):**
   * `exibir_status_carteira(estado, noticia)`: Desenha o painel financeiro estruturado e renderiza o noticiário do turno.
   * `exibir_menu_principal(opcoes)`: Mostra as opções e captura o input de decisão do jogador.

3. **`felipe_logica.py` (Processamento de Carteira):**
   * `atualizar_patrimonio_total(estado)`: Varre as ações possuídas, multiplica pela cotação atual do mercado e atualiza o patrimônio acumulado no topo de cada turno.
   * `calcular_compra(estado)` / `calcular_venda(estado)`: Valida saldos, executa as transações financeiras e altera as quantidades do dicionário.

4. **`nickollas_dados.py` (Banco de Dados Imutável):**
   * Armazena em estruturas de **Tuplas** fixas as matrizes de variação percentual de mercado e os textos das strings de notícias para os 12 meses.
   * `obter_taxas_mes(mes)` e `obter_noticia_mes(mes)`: Funções de consulta que extraem os dados estáticos.

5. **`nickollas_regras.py` (Motor de Sistema e Eventos):**
   * `simular_virada_de_mes(estado)`: Aplica as taxas mensais de volatilidade sobre os preços das ações ao mudar de turno e soma o aporte fixo de R$ 1.000,00.
   * `aplicar_evento_mercado(estado)`: O gatilho espião do **Mês 7**. Intercepta os preços e aplica a desvalorização punitiva de 15% nas empresas de tecnologia.
   * `verificar_vitoria_derrota(estado)`: Avalia se o cronômetro atingiu o limite e valida os critérios de encerramento.

---

## ⚙️ Funcionamento das Engrenagens do Código

### 📈 Mercado Dinâmico (Taxas Mensais)
Em vez de usar preços fixos digitados manualmente (*hardcoding*), o jogo calcula as oscilações de preço de forma puramente lógica. O arquivo `nickollas_dados.py` armazena multiplicadores flutuantes para cada ativo mês a mês (Ex: `1.20` indica ganho de 20%, `0.95` indica queda de 5%). 
Isso faz com que o mercado mude de comportamento a cada ciclo, exigindo que o jogador mude de estratégia em vez de apenas repetir compras na mesma ação.

### 📰 O Mecanismo de Notícias e Pistas
As notícias funcionam em uma linha de produção integrada:
1. No topo do turno, o `main.py` solicita ao `nickollas_dados.py` a string de texto correspondente ao `mes_atual`.
2. Essa mensagem traz uma pista contextual (Ex: *"Tensões internacionais indicam alta iminente nos combustíveis"*).
3. O `main.py` repassa esse texto para a função `exibir_status_carteira` da camada visual (`felipe_visual.py`).
4. O jogador analisa o texto e toma a decisão de compra ou venda antecipando a variação que ocorrerá no fechamento do mês.

### 🚨 O Gatilho do Mês 7 (Crash Cibernético)
Para dar sentido às funções do arquivo de regras do Nickollas sem gerar cálculos duplicados na tabela:
* As taxas no arquivo de dados para o Mês 7 são salvas como estáveis (`1.00`).
* Ao virar para o Mês 7, a função `aplicar_evento_mercado(estado)` é acionada pelo fluxo. Ela monitora o relógio e, ao detectar o gatilho, multiplica os preços vigentes de `NVIDIA`, `AAPL` e `MSFT` pelo fator multiplicador de `0.85`, simulando o impacto isolado do **Bug de Cibersegurança** em tempo de execução.

---

## 🔄 Fluxograma do Ciclo de Jogo (Mermaid Architecture)

O fluxo operacional do simulador roda seguindo a risca a seguinte árvore de processos:

```mermaid
---
config:
  layout: dagre
  theme: dark
  look: neo
---
graph TD
    Start([Início]) --> Init[main.py <br> Inicializa dicionário 'estado' <br> Saldo = 10000, Mês = 1]
    Init --> Loop[Início do Loop Mensal]
    
    Loop --> CalcPatr[Calcular Patrimônio Total <br> Saldo + Valor Atual dos Ativos]
    CalcPatr --> ShowUI[felipe_visual.py <br> Exibe Relatório e Notícias do Mês]
    ShowUI --> Menu{Escolha do Usuário}
    
    Menu -- "1. Comprar Ativo" --> Buy[felipe_logica.py <br> Deduz Saldo e aumenta Ações]
    Buy --> CalcPatr
    
    Menu -- "2. Vender Ativo" --> Sell[felipe_logica.py <br> Soma Saldo e reduz Ações]
    Sell --> CalcPatr
    
    Menu -- "3. Passar Mês" --> Check12{Mês Atual == 12?}
    
    Check12 -- Sim --> FinalCheck{Patrimônio Total >= R$ 25.000?}
    FinalCheck -- Sim --> Win([felipe_visual.py <br> Exibe Vitória])
    FinalCheck -- Não --> Lose([felipe_visual.py <br> Exibe Derrota])
    
    Check12 -- Não --> Aporte[nickollas_regras.py <br> Soma R$ 1.000 de salário ao Saldo]
    Aporte --> RunMarket[nickollas_regras.py / simular_virada_de_mes <br> Aplica as taxas mensais da matriz imutável]
    RunMarket --> IncMonth[Incrementa Mês: mes_atual += 1]
    IncMonth --> Check7{Mês Atual == 7?}
    
    Check7 -- Sim --> Crash[nickollas_regras.py / aplicar_evento_mercado <br> Intercepta e reduz 15 por cento das Techs]
    Crash --> Loop
    Check7 -- Não --> Loop