---
config:
  layout: dagre
  theme: dark
  look: neo
---
graph TD
    Start([Início]) --> Init[main.py <br> Inicializa dicionário 'estado' <br> Saldo = 10000, Mês = 1]
    Init --> Loop[Início do Loop Mensal]
    
    %% Bloco de Atualização e Exibição
    Loop --> CalcPatr[Calcular Patrimônio Total <br> Saldo + Valor Atual dos Ativos]
    CalcPatr --> ShowUI[felipe_visual.py <br> Exibe Relatório e Notícias do Mês]
    ShowUI --> Menu{Escolha do Usuário}
    
    %% Sub-loop de Ações (Não avança o mês)
    Menu -- "1. Comprar Ativo" --> Buy[felipe_logica.py <br> Deduz Saldo e aumenta Ações]
    Buy --> CalcPatr
    
    Menu -- "2. Vender Ativo" --> Sell[felipe_logica.py <br> Soma Saldo e reduz Ações]
    Sell --> CalcPatr
    
    %% Decisão de Fim de Turno
    Menu -- "3. Passar Mês" --> Check12{Mês Atual == 12?}
    
    %% Fluxo de Fim de Jogo
    Check12 -- Sim --> FinalCheck{Patrimônio Total >= R$ 25.000?}
    FinalCheck -- Sim --> Win([felipe_visual.py <br> Exibe Vitória])
    FinalCheck -- Não --> Lose([felipe_visual.py <br> Exibe Derrota])
    
    %% Fluxo de Avanço de Turno (Sua Nova Lógica Dinâmica)
    Check12 -- Não --> Aporte[nickollas_regras.py <br> Soma R$ 1.000 de salário ao Saldo]
    Aporte --> RunMarket[nickollas_regras.py / simular_virada_de_mes <br> Aplica as taxas mensais da matriz imutável]
    RunMarket --> IncMonth[Incrementa Mês: mes_atual += 1]
    IncMonth --> Check7{Mês Atual == 7?}
    
    %% O papel da função isolada aplicar_evento_mercado()
    Check7 -- Sim --> Crash[nickollas_regras.py / aplicar_evento_mercado <br> Intercepta e reduz 15 por cento das Techs]
    Crash --> Loop
    Check7 -- Não --> Loop

    style Init fill:#34495e,stroke:#3498db
    style Menu fill:#5d4037,stroke:#f1c40f
    style Check12 fill:#5d4037,stroke:#f1c40f
    style FinalCheck fill:#5d4037,stroke:#f1c40f
    style Check7 fill:#5d4037,stroke:#f1c40f
    style Win fill:#145a32,stroke:#27ae60
    style Lose fill:#78281f,stroke:#c0392b