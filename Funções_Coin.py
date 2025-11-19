from openpyxl import Workbook
from datetime import datetime

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



#------------------------------Opção 3-------------------------------



def listar_por_categoria(ws):
    print("\n----------------------------Listar por categoria-----------------------------")

    # escolher categoria
    while True:
        categoria_busca = input("Informe a categoria (lazer, alimento, trabalho, estudos): ").strip().lower()
        if categoria_busca in ["lazer", "alimento", "trabalho, estudos".replace(",", "")] and categoria_busca in ["lazer", "alimento", "trabalho", "estudos"]:
            break
        print("Categoria inválida. Tente novamente.")

    print(f"\nTransações da categoria: {categoria_busca}")
    print("ID | Valor | Tipo | Categoria | Data       | Descrição")
    print("-----------------------------------------------------------")

    encontrou = False
    total_saidas = 0.0
    qtd_saidas = 0

    for linha in ws.iter_rows(min_row=2, values_only=True):
        if not linha:
            continue

        tid, valor, tipo, categoria, descricao, dia, mes, ano = linha

        if categoria is None:
            continue

        # compara categoria ignorando maiúsculas/minúsculas
        if str(categoria).strip().lower() == categoria_busca:
            encontrou = True
            data_str = f"{int(dia):02d}/{int(mes):02d}/{int(ano)}"
            print(f"{tid} | {valor} | {tipo} | {categoria} | {data_str} | {descricao}")

            # se for saída, conta como gasto
            if tipo == "saida":
                total_saidas += float(valor)
                qtd_saidas += 1

    if not encontrou:
        print("Nenhuma transação encontrada para essa categoria.")
        return

    print("-----------------------------------------------------------")
    print(f"Total de GASTOS (saídas) na categoria '{categoria_busca}': R$ {total_saidas:.2f}")
    if qtd_saidas > 0:
        media_gastos = total_saidas / qtd_saidas
        print(f"MÉDIA de gasto por transação nessa categoria: R$ {media_gastos:.2f}")
    else:
        print("Não houve saídas (gastos) nessa categoria, portanto não há média de gastos.")




#------------------------------Opção 4-------------------------------



def listar_por_periodo(ws):
    print("\n----------------------------Listar transações por período-----------------------------")

    # Ler data inicial
    while True:
        data_ini_str = input("Informe a data inicial (DD/MM/AAAA): ").strip()
        try:
            data_inicial = datetime.strptime(data_ini_str, "%d/%m/%Y")
            break
        except:
            print("Data inválida. Use o formato DD/MM/AAAA.\n")

    # Ler data final
    while True:
        data_fim_str = input("Informe a data final (DD/MM/AAAA): ").strip()
        try:
            data_final = datetime.strptime(data_fim_str, "%d/%m/%Y")
            break
        except:
            print("Data inválida. Use o formato DD/MM/AAAA.\n")

    # Verificar se o período é válido
    if data_inicial > data_final:
        print("\nPeríodo inválido: a data inicial é maior que a final.")
        return

    print("\nTransações dentro do período:")
    print("ID | Valor | Tipo | Categoria | Data       | Descrição")
    print("-----------------------------------------------------------")

    encontrou = False
    total_saidas = 0.0
    qtd_saidas = 0



    for linha in ws.iter_rows(min_row=2, values_only=True):
        if not linha:
            continue

        tid, valor, tipo, categoria, descricao, dia, mes, ano = linha

        if dia is None or mes is None or ano is None or valor is None:
            continue

        # montar a data real da transação
        try:
            data_transacao = datetime(int(ano), int(mes), int(dia))
        except:
            continue  # ignora datas inválidas

        # verificar se está dentro do período
        if data_inicial <= data_transacao <= data_final:
            encontrou = True
            data_str = data_transacao.strftime("%d/%m/%Y")
            print(f"{tid} | {valor} | {tipo} | {categoria} | {data_str} | {descricao}")

            # se for saída, conta como gasto
            if tipo == "saida":
                total_saidas += float(valor)
                qtd_saidas += 1

    print("-----------------------------------------------------------")

    if not encontrou:
        print("Nenhuma transação encontrada nesse período.")
        return

    print(f"Total de GASTOS (saídas) no período: R$ {total_saidas:.2f}")
    if qtd_saidas > 0:
        media_gastos = total_saidas / qtd_saidas
        print(f"MÉDIA de gasto por transação no período: R$ {media_gastos:.2f}")
    else:
        print("Não houve saídas (gastos) no período, portanto não há média de gastos.")



#------------------------------Opção 5-------------------------------



from datetime import datetime

def calcular_saldo_periodo(ws):
    print("\n----------------------------Saldo por período-----------------------------")

    # Ler data inicial usando datetime
    while True:
        data_ini_str = input("Informe a data inicial (DD/MM/AAAA): ").strip()
        try:
            data_inicial = datetime.strptime(data_ini_str, "%d/%m/%Y")
            break
        except:
            print("Data inválida. Use o formato DD/MM/AAAA.\n")

    # Ler data final usando datetime
    while True:
        data_fim_str = input("Informe a data final (DD/MM/AAAA): ").strip()
        try:
            data_final = datetime.strptime(data_fim_str, "%d/%m/%Y")
            break
        except:
            print("Data inválida. Use o formato DD/MM/AAAA.\n")

    # Verificar se o período é válido
    if data_inicial > data_final:
        print("\nPeríodo inválido: a data inicial é maior que a final.")
        return

    saldo = 0.0
    total_entradas = 0.0
    total_saidas = 0.0
    encontrou = False

    # dicionário para saldo por mês: chave = (ano, mes), valor = saldo desse mês
    saldo_por_mes = {}  # ex: {(2025, 1): 150.0, (2025, 2): -20.0}

    # Percorrer as linhas da planilha
    for linha in ws.iter_rows(min_row=2, values_only=True):

        if not linha:
            continue

        tid, valor, tipo, categoria, descricao, dia, mes, ano = linha

        # pular linhas vazias
        if dia is None or mes is None or ano is None or valor is None or tipo is None:
            continue

        # montar a data real da transação
        try:
            data_transacao = datetime(int(ano), int(mes), int(dia))
        except:
            continue  # ignora datas mal formatadas na planilha

        # comparar datas usando datetime
        if data_inicial <= data_transacao <= data_final:
            encontrou = True
            valor_f = float(valor)

            chave_mes = (int(ano), int(mes))
            if chave_mes not in saldo_por_mes:
                saldo_por_mes[chave_mes] = 0.0

            if tipo == "entrada":
                total_entradas += valor_f
                saldo += valor_f
                saldo_por_mes[chave_mes] += valor_f

            elif tipo == "saida":
                total_saidas += valor_f
                saldo -= valor_f
                saldo_por_mes[chave_mes] -= valor_f

    print("\n================== RESULTADO DO PERÍODO ==================")
    print(f"Período: {data_inicial.strftime('%d/%m/%Y')}  até  {data_final.strftime('%d/%m/%Y')}")
    print("----------------------------------------------------------")

    if not encontrou:
        print("Nenhuma transação encontrada nesse período.")
        return

    # Totais gerais do período
    print(f"Total de ENTRADAS: R$ {total_entradas:.2f}")
    print(f"Total de SAÍDAS..: R$ {total_saidas:.2f}")
    print("----------------------------------------------------------")
    print(f"SALDO NO PERÍODO.: R$ {saldo:.2f}")

    # Saldo por mês
    print("\n================== SALDO POR MÊS ==================")
    # ordenar por ano, depois por mês
    chaves_ordenadas = sorted(saldo_por_mes.keys())  # ordena por (ano, mes)

    for (ano_m, mes_m) in chaves_ordenadas:
        saldo_mes = saldo_por_mes[(ano_m, mes_m)]
        print(f"Mês {mes_m:02d}/{ano_m}: R$ {saldo_mes:.2f}")
