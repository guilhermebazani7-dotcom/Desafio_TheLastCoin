from openpyxl import Workbook

def criar_planilha():
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

    # salva o arquivo vazio com o cabeçalho
    wb.save("Controle_Financeiro.xlsx")
    return wb, ws


def adicionar_transa(wb, ws):
    print("----------------------------Cadastro de transações-----------------------------")

    id_transacao = 1

    while True:

        print(f"\nRegistrando transação de ID {id_transacao}...\n")

        # Cadastrando o Valor
        while True:
            valor_numero = input("Digite o valor da transação: ")
            valor_numero = valor_numero.replace(",", ".")
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
            categoria = input("Categoria (lazer, alimento, trabalho, estudos): ").strip().lower()
            if categoria in ["lazer", "alimento", "trabalho", "estudos"]:
                break
            print("Categoria inválida.")

        # Cadastrando Descrição
        while True:
            descricao = input("Descrição: ").strip()
            if descricao != "":
                break
            print("Descrição não pode ser vazia.")

        # Cadastrando o Dia
        while True:
            dia_numero = input("Dia (1 a 30): ")
            if dia_numero.isdigit() and 1 <= int(dia_numero) <= 30:
                dia = int(dia_numero)
                break
            print("Dia inválido.")

        # Cadastrando Mês
        while True:
            mes_numero = input("Mês (1 a 12): ")
            if mes_numero.isdigit() and 1 <= int(mes_numero) <= 12:
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

        ws.append([id_transacao, valor, tipo, categoria, descricao, dia, mes, ano])
        wb.save("Controle_Financeiro.xlsx")
        print("Transação salva com sucesso!")

        id_transacao += 1

        continuar = input("\nDeseja registrar outra transação? (s/n): ").lower().strip()
        if continuar != "s":
            print("Encerrando cadastro.")
            break

    print("Arquivo atualizado: Controle_Financeiro.xlsx")



#------------------------------Opção 2------------------------------



def remover_transa(wb, ws):
    print("\n----------------------------Remover transação-----------------------------")

    # Mostrar uma listagem simples das transações (opcional, mas ajuda o usuário)
    print("\nTransações cadastradas:")
    print("ID | Valor | Tipo | Categoria | Dia/Mês/Ano | Descrição")
    print("-----------------------------------------------------------")

    linhas = list(ws.iter_rows(min_row=2, values_only=True))
    if not linhas:
        print("Nenhuma transação encontrada.")
        return

    for linha in linhas:
        tid, valor, tipo, categoria, descricao, dia, mes, ano = linha
        print(f"{tid} | {valor} | {tipo} | {categoria} | {dia}/{mes}/{ano} | {descricao}")

    print("-----------------------------------------------------------")

    # Pedir o ID a remover
    id_str = input("\nInforme o ID da transação que deseja remover: ").strip()

    if not id_str.isdigit():
        print("ID inválido. Deve ser um número inteiro.")
        return

    id_remover = int(id_str)

    # Procurar o ID na planilha
    encontrou = False
    for indice_linha, row in enumerate(ws.iter_rows(min_row=2), start=2):
        cell_id = row[0].value  # primeira coluna é o ID
        if cell_id == id_remover:
            encontrou = True
            # Mostrar os dados antes de remover (opcional)
            valor = row[1].value
            tipo = row[2].value
            categoria = row[3].value
            descricao = row[4].value
            dia = row[5].value
            mes = row[6].value
            ano = row[7].value

            print("\nTransação encontrada:")
            print(f"ID: {cell_id}")
            print(f"Valor: {valor}")
            print(f"Tipo: {tipo}")
            print(f"Categoria: {categoria}")
            print(f"Data: {dia}/{mes}/{ano}")
            print(f"Descrição: {descricao}")

            confirma = input("Deseja realmente remover essa transação? (s/n): ").strip().lower()
            if confirma == "s":
                ws.delete_rows(indice_linha, 1)
                wb.save("Controle_Financeiro.xlsx")
                print("Transação removida com sucesso!")
            else:
                print("Remoção cancelada.")
            break

    if not encontrou:
        print("Nenhuma transação com esse ID foi encontrada.")



#------------------------------Opção 5-------------------------------



def calcular_saldo_periodo(ws):
    print("\n----------------------------Saldo por período-----------------------------")

    # Ler data inicial
    print("Informe a DATA INICIAL do período:")
    while True:
        dia_ini_str = input("Dia inicial (1 a 30): ")
        mes_ini_str = input("Mês inicial (1 a 12): ")
        ano_ini_str = input("Ano inicial (0 a 2025): ")

        if (dia_ini_str.isdigit() and mes_ini_str.isdigit() and ano_ini_str.isdigit()):
            dia_ini = int(dia_ini_str)
            mes_ini = int(mes_ini_str)
            ano_ini = int(ano_ini_str)

            if 1 <= dia_ini <= 30 and 1 <= mes_ini <= 12 and 0 <= ano_ini <= 2025:
                break
        print("Data inicial inválida. Tente novamente.\n")

    # Ler data final
    print("\nInforme a DATA FINAL do período:")
    while True:
        dia_fim_str = input("Dia final (1 a 30): ")
        mes_fim_str = input("Mês final (1 a 12): ")
        ano_fim_str = input("Ano final (0 a 2025): ")

        if (dia_fim_str.isdigit() and mes_fim_str.isdigit() and ano_fim_str.isdigit()):
            dia_fim = int(dia_fim_str)
            mes_fim = int(mes_fim_str)
            ano_fim = int(ano_fim_str)

            if 1 <= dia_fim <= 30 and 1 <= mes_fim <= 12 and 0 <= ano_fim <= 2025:
                break
        print("Data final inválida. Tente novamente.\n")

    # Converter datas para número AAAAMMDD para facilitar comparação
    data_ini_num = ano_ini * 10000 + mes_ini * 100 + dia_ini
    data_fim_num = ano_fim * 10000 + mes_fim * 100 + dia_fim

    if data_ini_num > data_fim_num:
        print("\nPeríodo inválido: a data inicial é maior que a final.")
        return

    # Cálculo do saldo
    saldo = 0.0
    total_entradas = 0.0
    total_saidas = 0.0
    encontrou = False

    # Lembrando a ordem das colunas:
    # 0: ID
    # 1: Valor
    # 2: Tipo ("entrada" ou "saida")
    # 3: Categoria
    # 4: Descricao
    # 5: Dia
    # 6: Mes
    # 7: Ano

    for linha in ws.iter_rows(min_row=2, values_only=True):
        if not linha:
            continue

        tid, valor, tipo, categoria, descricao, dia, mes, ano = linha

        if dia is None or mes is None or ano is None:
            continue

        data_num = int(ano) * 10000 + int(mes) * 100 + int(dia)

        if data_ini_num <= data_num <= data_fim_num:
            encontrou = True
            if tipo == "entrada":
                total_entradas += float(valor)
                saldo += float(valor)
            elif tipo == "saida":
                total_saidas += float(valor)
                saldo -= float(valor)

    print("\n================== RESULTADO DO PERÍODO ==================")
    print(f"Período: {dia_ini}/{mes_ini}/{ano_ini}  até  {dia_fim}/{mes_fim}/{ano_fim}")

    if not encontrou:
        print("Nenhuma transação encontrada nesse período.")
        return

    print(f"Total de ENTRADAS: R$ {total_entradas:.2f}")
    print(f"Total de SAÍDAS..: R$ {total_saidas:.2f}")
    print("-------------------------------------------------")
    print(f"SALDO NO PERÍODO.: R$ {saldo:.2f}")


