from nickollas_teixeira import registrar_historico

def atualizar_patrimonio_total(estado: dict):
    """
    Calcula o patrimônio total do jogador no início do turno.
    Soma o dinheiro líquido em caixa com o valor de mercado atualizado de todas as ações.
    """
    valor_acoes = 0.0
    
    # Varre a carteira verificando quantas ações o usuário tem e multiplica pelo preço do mês atual
    for acao, quantidade in estado["carteira_quantidades"].items():
        preco_atual = estado["precos_mercado"][acao]
        valor_acoes += quantidade * preco_atual
        
    # O patrimônio total é o dinheiro vivo + o valor do capital investido
    estado["patrimonio_total"] = estado["saldo_disponivel"] + valor_acoes
    return estado


def exibir_menu_principal(opcoes: tuple) -> str:
    """Exibe as opções do simulador e captura a escolha do usuário."""
    print("Menu Principal:")
    # Usa enumerate para gerar os números das opções automaticamente (1, 2, 3...)
    for i, opcao in enumerate(opcoes, start=1):
        print(f"{i}. {opcao}")
    
    escolha = input("Escolha uma opção (1, 2 ou 3): ")
    return escolha
    

def exibir_status_carteira(estado: dict, noticia_atual: str = ""):
    """
    Renderiza o dashboard do simulador no terminal.
    Mostra o mês, a notícia que serve de pista, o saldo e o lucro/prejuízo dinâmico.
    """
    print("==================================================================================")
    print(f" 📅 MÊS ATUAL: {estado['mes_atual']} / 12")
    print("==================================================================================")
    print(" 📰 NOTICIÁRIO DA FARIA LIMA:")
    print(f"  > {noticia_atual}")
    print("==================================================================================")
    print(f"  Patrimônio Total: R$ {estado['patrimonio_total']:.2f}")
    print(f"  Saldo Disponível: R$ {estado['saldo_disponivel']:.2f}")
    print("==================================================================================")
    
    # Calcula todo o dinheiro que entrou no jogo (10k iniciais + 1k por mês passado)
    capital_investido = 10000.0 + (estado['mes_atual'] - 1) * 1000.0
    
    # Compara o patrimônio com o capital investido real, e não com 10.000 fixos
    if estado['patrimonio_total'] > capital_investido:
        print(f"Lucro: R$ {estado['patrimonio_total'] - capital_investido:.2f}")

    elif estado['patrimonio_total'] < capital_investido:
        print(f"Prejuízo: R$ {capital_investido - estado['patrimonio_total']:.2f}")
    
    elif estado["mes_atual"] > 1:
        print("Situação: Estável (R$ 0.00 de variação)")
        
    print(f"Mês Atual: {estado['mes_atual']}")
    print("Carteira de Ações:")
    
    acoes_possuidas = False
    # Itera sobre a carteira e só exibe as ações que o usuário realmente possui (quantidade > 0)
    for acao, quantidade in estado['carteira_quantidades'].items():
        if quantidade > 0:
            print(f"  {acao}: {quantidade} ações (Preço: R$ {estado['precos_mercado'][acao]:.2f})")
            acoes_possuidas = True
            
    if not acoes_possuidas:
        print("  Nenhuma ação possuída.")
    print("==================================================================================")


def calcular_compra(historico: list, estado: dict) -> dict:
    """
    Gerencia a lógica de compra de ações.
    Possui travas de segurança para evitar compras sem saldo e tratamento de exceções para inputs inválidos.
    """
    print("Você escolheu comprar ações, muito bem! Vamos lá.")

    # Trava de segurança 1: Impede o jogador de tentar comprar se estiver zerado
    if estado["saldo_disponivel"] <= 0:
        print("Saldo insuficiente para realizar compras. Operação cancelada.")
        return estado

    print("Aqui estão os preços atuais de mercado:")
    for acao, preco in estado["precos_mercado"].items():
        print(f"  {acao}: R$ {preco:.2f}")

    # Loop de validação do nome da ação
    while True:
        acao_escolhida = input("Digite o nome da ação que deseja comprar: ").strip().upper()

        if acao_escolhida not in estado["precos_mercado"]:
            print("Ação inválida. Operação cancelada.")
            print("Por favor, escolha uma ação válida da lista.")
        else:
            break  
        
    # Loop de validação da quantidade (com proteção contra quebra de código)
    while True:
        try:
            # Tenta converter a digitação para número inteiro
            quantidade_compra = int(input("Digite a quantidade de ações que deseja comprar: "))
            
            # Trava de segurança 2: Impede números negativos ou zero
            if quantidade_compra <= 0:
                print("Quantidade inválida. Por favor, insira uma quantidade positiva.")
            else:
                custo_total = quantidade_compra * estado["precos_mercado"][acao_escolhida]
                
                # Trava de segurança 3: Validação financeira
                if custo_total > estado["saldo_disponivel"]:
                    print(f"Saldo insuficiente. Você precisa de R$ {custo_total:.2f} mas tem apenas R$ {estado['saldo_disponivel']:.2f}.")
                else:
                    break  # Sai do loop se passou em todas as validações
                    
        except ValueError:
            # Captura o erro caso o usuário digite texto (ex: "dez") em vez de números, evitando crash do sistema
            print("Erro: Digite apenas números inteiros!")
            print("Por favor, insira uma quantidade válida.")

    # Efetiva a transação no dicionário de estado
    estado["saldo_disponivel"] -= custo_total
    estado["carteira_quantidades"][acao_escolhida] += quantidade_compra 
    
    print(f"Compra de {quantidade_compra} ações de {acao_escolhida} realizada com sucesso!")
    print(f"Saldo disponível após a compra: R$ {estado['saldo_disponivel']:.2f}")
    
    #registra o histórico da compra para análises futuras
    registrar_historico(historico, f"Compra {quantidade_compra} {acao_escolhida}", estado)
    return estado
    

def calcular_venda(historico: list, estado: dict) -> dict:
    """
    Gerencia a lógica de venda de ações.
    Verifica se o usuário possui a ação em carteira antes de permitir a venda.
    """
    print("Você escolheu vender ações, muito bem! Vamos lá.")
    print("Aqui estão as ações que você possui:")
    
    possui_acoes = False
    for acao, quantidade in estado["carteira_quantidades"].items():
        if quantidade > 0:
            print(f"  {acao}: {quantidade} ações (Preço: R$ {estado['precos_mercado'][acao]:.2f})")
            possui_acoes = True
            
    # Trava de segurança 1: Bloqueia a venda se a carteira estiver completamente vazia
    if not possui_acoes:
        print("  Nenhuma ação possuída.")
        print("Operação de venda cancelada.")
        return estado
    
    # Loop de validação do nome da ação
    while True:
        acao_escolhida = input("Digite o nome da ação que deseja vender: ").strip().upper()

        if acao_escolhida not in estado["carteira_quantidades"]:
            print("Ação inválida. Operação cancelada.")
            print("Por favor, escolha uma ação válida da lista.")
        # Trava de segurança 2: Verifica se o usuário tem saldo em custódia daquela ação específica
        elif estado["carteira_quantidades"][acao_escolhida] <= 0:
            print("Você não possui ações dessa empresa para vender. Operação cancelada.")
            print("Por favor, escolha uma ação da qual você possua ações para vender.")
        else:
            break
            
    # Loop de validação da quantidade a ser vendida
    while True:
        try:
            quantidade_venda = int(input("Digite a quantidade de ações que deseja vender: "))
            
            if quantidade_venda <= 0:
                print("Quantidade inválida. Operação cancelada.")
                print("Por favor, insira uma quantidade positiva.")
            # Trava de segurança 3: Impede o jogador de vender mais ações do que realmente possui (Short Selling não permitido)
            elif quantidade_venda > estado["carteira_quantidades"][acao_escolhida]:
                print("Quantidade de ações insuficiente. Operação cancelada.")
                print("Por favor, insira uma quantidade menor ou igual à quantidade de ações possuídas.")
            else:
                break
        except ValueError:
            # Proteção contra erros de digitação de strings
            print("Erro: Digite apenas números inteiros!")
            print("Por favor, insira uma quantidade válida.")
    
    # Efetiva a transação matemática de venda no estado
    estado["carteira_quantidades"][acao_escolhida] -= quantidade_venda
    valor_total = quantidade_venda * estado["precos_mercado"][acao_escolhida]
    estado["saldo_disponivel"] += valor_total
    
    print(f"Venda de {quantidade_venda} ações de {acao_escolhida} realizada com sucesso!")
    print(f"Saldo disponível após a venda: R$ {estado['saldo_disponivel']:.2f}")
    
    registrar_historico(historico, f"Venda {quantidade_venda} {acao_escolhida}", estado)
    return estado