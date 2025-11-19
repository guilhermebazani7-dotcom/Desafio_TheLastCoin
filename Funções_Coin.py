from openpyxl import Workbook

wb = Workbook()
ws = wb.active
ws.title = "Transacoes"

ws.append([
    "ID",
    "Valor",
    "Tipo",
    "Categoria",
    "Descricao",
    "Dia",
    "Mes",
    "Ano"
])

print("----------------------------Cadastro de transações-----------------------------")

id_transacao = 1

while True:

    print(f"\nRegistrando transação de ID {id_transacao}...\n")

    # Cadastrando o Valor
    while True:
        valor_numero = input("Digite o valor da transação: ")
        valor_numero = valor_numero.replace(",", ".")   #Isso aq vai tratar caso tenha vírgula
        try:
            valor = float(valor_numero)
            if valor > 0:
                break
            print("O valor deve ser maior que zero.")
        except:
            print("Valor inválido. Tente novamente.")

    # Cadastrando o Tipo
    while True:
        tipo_transa = input("Digite o tipo da transação (1 - entrada, 2 - saída): ")
        if tipo_transa == "1":
            tipo = "entrada"
            break
        elif tipo_transa == "2":
            tipo = "saida"
            break
        else:
            print("Opção inválida. Digite 1 ou 2.")

    # Cadastrando Categoria
    while True:
        categoria = input("Categoria (lazer, alimento, trabalho, estudos): ").strip().lower()   #trata espaços e maiusculos
        if categoria in ["lazer", "alimento", "trabalho", "estudos"]:
            break
        print("Categoria inválida.")

    # Cadastrando Descrição
    while True:
        descricao = input("Descrição: ").strip()      #trata espaços
        if descricao != "":          #interpreta que tem que ter uma descrição
            break
        print("Descrição não pode ser vazia.")

    # Cadastrando o Dia
    while True:
        dia_numero = input("Dia (1 a 30): ")
        if dia_numero.isdigit() and 1 <= int(dia_numero) <= 30:     #põe os limites de 1 a 30 (mês)
            dia = int(dia_numero)
            break
        print("Dia inválido.")

    # Cadastrando Mês
    while True:
        mes_numero = input("Mês (1 a 12): ")
        if mes_numero.isdigit() and 1 <= int(mes_numero) <= 12:        #esse .isdigit() faz tudo virar número
            mes = int(mes_numero)
            break
        print("Mês inválido.")

    # Cadastrando Ano
    while True:
        ano_numero = input("Ano (0 a 2025): ")
        if ano_numero.isdigit() and 1 <= int(ano_numero) <= 2025:
            ano = int(ano_numero)
            break
        print("Ano inválido.")

    ws.append([id_transacao, valor, tipo, categoria, descricao, dia, mes, ano])     #adiciona as mudanças
    wb.save("Controle_Financeiro.xlsx")          #salva
    print("Transação salva com sucesso!")

    id_transacao += 1

    continuar = input("\nDeseja registrar outra transação? (s/n): ").lower().strip()
    if continuar != "s":
        print("Encerrando cadastro.")
        break

print("Arquivo atualizado: Controle_Financeiro.xlsx")
