from felipe_allan import exibir_menu_principal, exibir_status_carteira, calcular_compra, calcular_venda


def main():
    while True:
        opcao = exibir_menu_principal()
        if opcao == "1":
            exibir_status_carteira()
        elif opcao == "2":
            calcular_compra()
        elif opcao == "3":
            calcular_venda()
        elif opcao == "4":
            print("Saindo do programa...")
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()  