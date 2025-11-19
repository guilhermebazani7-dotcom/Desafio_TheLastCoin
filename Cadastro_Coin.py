from Funções_Coin import criar_planilha, adicionar_transa, remover_transa, calcular_saldo_periodo


usuarios = {}  # dicionário em memória: {nome: senha}


def cadastrar_usuario():
    print("--------- CADASTRO ---------")
    nome = input("Digite um nome de usuário: ").strip()
    if nome == "":
        print("Nome de usuário não pode ser vazio.")
        return
    if nome in usuarios:
        print("Usuário já existe. Tente outro nome.")
        return

    senha = input("Digite uma senha: ").strip()
    if senha == "":
        print("Senha não pode ser vazia.")
        return

    usuarios[nome] = senha
    print(f"Usuário '{nome}' cadastrado com sucesso!")


def fazer_login():
    print("\n--------- LOGIN ---------")
    nome = input("Usuário: ").strip()
    senha = input("Senha: ").strip()

    if nome in usuarios and usuarios[nome] == senha:
        print(f"Login bem-sucedido! Bem-vindo, {nome}.")
        return nome
    else:
        print("Usuário ou senha inválidos.")
        return None


def menu_inicial():
    while True:
        print("\n================= MENU INICIAL =================")
        print("1 - Cadastrar novo usuário")
        print("2 - Login")
        print("0 - Sair")

        escolha = input("Escolha uma opção: ")

        if escolha == "1":
            cadastrar_usuario()

        elif escolha == "2":
            usuario_logado = fazer_login()
            if usuario_logado is not None:
                # ---------- MENU FINANCEIRO (APÓS LOGIN) ----------
                # cria a planilha e obtém wb e ws
                wb, ws = criar_planilha()

                while True:
                    print(f"\n========== MENU FINANCEIRO ({usuario_logado}) ==========")
                    print("1 - Adicionar transação")
                    print("2 - Remover transação")
                    print("3 - Listar transações por categoria (a implementar)")
                    print("4 - Listar transações por período (a implementar)")
                    print("5 - Calcular saldo por período")
                    print("0 - Voltar ao menu inicial")

                    opcao_fin = input("Escolha uma opção: ")

                    if opcao_fin == "1":
                        # chama a função que você já criou em Funções_Coin.py
                        adicionar_transa(wb, ws)

                    elif opcao_fin == "2":
                        remover_transa(wb, ws)

                    elif opcao_fin == "3":
                        print("Função de listar transações por categoria ainda será implementada.")

                    elif opcao_fin == "4":
                        print("Função de listar transações por período ainda será implementada.")

                    elif opcao_fin == "5":
                        calcular_saldo_periodo(ws)

                    elif opcao_fin == "0":
                        print("Voltando ao menu inicial...")
                        break

                    else:
                        print("Opção inválida. Tente novamente.")

        elif escolha == "0":
            print("Encerrando o sistema de usuários.")
            break

        else:
            print("Opção inválida. Tente novamente.")


# ------------------ INÍCIO DO PROGRAMA ------------------

if __name__ == "__main__":
    print("----------------------------Sistema de Usuários-----------------------------")
    menu_inicial()
