
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
                # 🔹 AQUI você vai chamar o menu financeiro
                # Exemplo depois:
                # from sistema_financeiro import menu_financeiro
                # menu_financeiro(usuario_logado)
                print("Aqui você chamaria o menu financeiro em outro módulo.")
                # por enquanto só volta pro menu inicial

        elif escolha == "0":
            print("Encerrando o sistema de usuários.")
            break

        else:
            print("Opção inválida. Tente novamente.")


# ------------------ INÍCIO DO PROGRAMA ------------------

if __name__ == "__main__":
    print("----------------------------Sistema de Usuários-----------------------------")
    menu_inicial()
