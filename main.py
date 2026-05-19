# Orquestrador do Sistema - Faria Lima Simulator
# Responsável por controlar o fluxo principal e a passagem do dicionário 'estado' entre os módulos.

from felipe_allan import (
    exibir_menu_principal, 
    exibir_status_carteira, 
    calcular_compra, 
    calcular_venda,
    atualizar_patrimonio_total  
)
from nickollas_teixeira import (
    aplicar_evento_mercado, 
    obter_precos_mes, 
    obter_noticia_mes,
    verificar_vitoria_derrota,
    simular_virada_de_mes       
)

def main():
    # Dicionário de Estado Central: Substitui o uso de variáveis globais.
    # É passado e modificado por referência ao longo de todas as funções do sistema.
    estado: dict = {
        "saldo_disponivel": 10000.0,
        "patrimonio_total": 10000.0,
        "mes_atual": 1,
        "carteira_quantidades": {"NVIDIA": 0, "AAPL": 0, "MSFT": 0, "PETR4": 0, "VALE3": 0},
        "precos_mercado": {"NVIDIA": 100.0, "AAPL": 100.0, "MSFT": 100.0, "PETR4": 100.0, "VALE3": 100.0},
    }
    
    # Estrutura imutável para as opções do menu
    opcoes = ("Comprar Ações", "Vender Ações", "Passar Mês")
    historico = []  # Lista para armazenar o histórico de jogadas, pode ser usada para análises futuras
    print("Bem-vindo ao Simulador de Investimentos!")
    print("Tente alcançar o objetivo de mais de R$ 25.000 em 12 meses.\n")

    # LOOP PRINCIPAL DO JOGO
    # A função verificar_vitoria_derrota funciona como o "juiz", retornando True apenas no final do mês 12.
    while not verificar_vitoria_derrota(estado):
        
        # 1. Consolida a posição da carteira logo no início do turno para evitar dados desatualizados
        estado = atualizar_patrimonio_total(estado)
        
        # 2. Resgata a pista textual do mês no arquivo de dados para guiar o jogador
        noticia_atual = obter_noticia_mes(estado["mes_atual"])

        # 3. Renderiza a tela limpa com os dados calculados
        exibir_status_carteira(estado, noticia_atual)
        
        # 4. Aguarda a tomada de decisão do usuário
        escolha = exibir_menu_principal(opcoes) 
        
        # 5. Roteamento de fluxo com base na entrada do usuário
        if escolha == "1":
            # Sub-loop de compra: Altera o estado, mas não avança o tempo
            estado = calcular_compra(historico, estado)
            
        elif escolha == "2":
            # Sub-loop de venda: Altera o estado, mas não avança o tempo
            estado = calcular_venda(historico, estado)

            
        elif escolha == "3":
            # Avanço de tempo: Dispara as engrenagens de mercado
            estado = simular_virada_de_mes(estado)
            estado = aplicar_evento_mercado(estado)

        else:
            # Fallback de segurança para escolhas que não sejam 1, 2 ou 3
            print("Opção inválida. Por favor, escolha 1, 2 ou 3.")
    
    #Antes do fim do jogo exibe histórico completo para o usuário analisar suas decisões ao longo dos meses
    print("\nHistórico de Jogadas:")
    for registro in historico:
        print(f"Mês {registro['mes']}: Escolha - {registro['escolha']}, Saldo - R$ {registro['saldo_disponivel']:.2f}, Patrimônio - R$ {registro['patrimonio_total']:.2f}")
        print(f"Carteira: {registro['carteira_quantidades']}, Preços: {registro['precos_mercado']}")
        print("----------------------------------------------------------------------------------")

    print("Obrigado por jogar o Simulador de Investimentos da Faria Lima!")
    print("Esperamos que tenha aprendido algo sobre o mercado financeiro e a importância de decisões estratégicas.")
    print("Até a próxima! 🚀")
    # Break do loop indica que a condição de fim de jogo foi atingida
    print("Fim de jogo!")

if __name__ == "__main__":
    main()