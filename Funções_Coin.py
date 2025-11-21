import os
from openpyxl import Workbook, load_workbook
from datetime import datetime


def criar_planilha():
    """
    Abre o arquivo Controle_Financeiro.xlsx se ele existir.
    Se não existir, cria um novo com a planilha Transacoes e o cabeçalho.
    Retorna wb, ws.
    """
    arquivo = "Controle_Financeiro.xlsx"

    if os.path.exists(arquivo):
        # Arquivo já existe: apenas abre
        wb = load_workbook(arquivo)
        # Tenta usar a planilha "Transacoes"; se não existir, usa a ativa
        if "Transacoes" in wb.sheetnames:
            ws = wb["Transacoes"]
        else:
            ws = wb.active
            ws.title = "Transacoes"
            # Se a planilha estiver vazia, garante o cabeçalho
            if ws.max_row == 1 and all(c.value is None for c in ws[1]):
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
                wb.save(arquivo)
    else:
        # Arquivo não existe: cria do zero
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

        wb.save(arquivo)

    return wb, ws


def adicionar_transa(wb, ws):
    print("----------------------------Cadastro de transações-----------------------------")

    # Descobrir o maior ID já usado na planilha, para continuar a contagem
    max_id = 0
    for linha in ws.iter_rows(min_row=2, max_col=1, values_only=True):
        cell_id = linha[0]
        if cell_id is None:
            continue
        try:
            iid = int(cell_id)
            if iid > max_id:
                max_id = iid
        except:
            continue

    id_transacao = max_id + 1  # próximo ID disponível

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
# AGORA NÃO TEM MAIS input()/print(), SÓ REMOVE PELO ID RECEBIDO


def remover_transa(wb, ws, id_remover):
    """
    Remove a transação com o ID informado.
    Retorna:
      (True, detalhes) se encontrou e removeu
      (False, mensagem) se não encontrou
    """
    for indice_linha, row in enumerate(ws.iter_rows(min_row=2), start=2):
        cell_id = row[0].value  # primeira coluna é o ID
        if cell_id == id_remover:
            valor = row[1].value
            tipo = row[2].value
            categoria = row[3].value
            descricao = row[4].value
            dia = row[5].value
            mes = row[6].value
            ano = row[7].value

            detalhes = (
                f"ID: {cell_id}\n"
                f"Valor: {valor}\n"
                f"Tipo: {tipo}\n"
                f"Categoria: {categoria}\n"
                f"Data: {dia}/{mes}/{ano}\n"
                f"Descrição: {descricao}"
            )

            ws.delete_rows(indice_linha, 1)
            wb.save("Controle_Financeiro.xlsx")
            return True, detalhes

    return False, "Nenhuma transação com esse ID foi encontrada."



#------------------------------Opção 3-------------------------------


def listar_por_categoria(ws, categoria_busca):
    categoria_busca = str(categoria_busca).strip().lower()

    # validação simples
    if categoria_busca not in ["lazer", "alimento", "trabalho", "estudos"]:
        msg = "Categoria inválida. Use: lazer, alimento, trabalho ou estudos."
        print(msg)
        return msg

    linhas_resultado = []
    linhas_resultado.append(f"Transações da categoria: {categoria_busca}")
    linhas_resultado.append("ID | Valor | Tipo | Categoria | Data       | Descrição")
    linhas_resultado.append("-----------------------------------------------------------")

    print("\n----------------------------Listar por categoria-----------------------------")
    print(f"Categoria buscada: {categoria_busca}")
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
            texto = f"{tid} | {valor} | {tipo} | {categoria} | {data_str} | {descricao}"
            print(texto)
            linhas_resultado.append(texto)

            # se for saída, conta como gasto
            if tipo == "saida":
                total_saidas += float(valor)
                qtd_saidas += 1

    if not encontrou:
        msg = "Nenhuma transação encontrada para essa categoria."
        print(msg)
        return msg

    linhas_resultado.append("-----------------------------------------------------------")
    print("-----------------------------------------------------------")
    linhas_resultado.append(f"Total de GASTOS (saídas) na categoria '{categoria_busca}': R$ {total_saidas:.2f}")
    print(f"Total de GASTOS (saídas) na categoria '{categoria_busca}': R$ {total_saidas:.2f}")

    if qtd_saidas > 0:
        media_gastos = total_saidas / qtd_saidas
        linhas_resultado.append(f"MÉDIA de gasto por transação nessa categoria: R$ {media_gastos:.2f}")
        print(f"MÉDIA de gasto por transação nessa categoria: R$ {media_gastos:.2f}")
    else:
        linhas_resultado.append("Não houve saídas (gastos) nessa categoria, portanto não há média de gastos.")
        print("Não houve saídas (gastos) nessa categoria, portanto não há média de gastos.")

    return "\n".join(linhas_resultado)



#------------------------------Opção 4-------------------------------


def listar_por_periodo(ws, data_inicial, data_final):
    """
    data_inicial e data_final são objetos datetime já validados.
    """
    print("\n----------------------------Listar transações por período-----------------------------")

    # Verificar se o período é válido
    if data_inicial > data_final:
        msg = "Período inválido: a data inicial é maior que a final."
        print(msg)
        return msg

    linhas_resultado = []
    linhas_resultado.append(f"Transações de {data_inicial.strftime('%d/%m/%Y')} até {data_final.strftime('%d/%m/%Y')}")
    linhas_resultado.append("ID | Valor | Tipo | Categoria | Data       | Descrição")
    linhas_resultado.append("-----------------------------------------------------------")

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
            texto = f"{tid} | {valor} | {tipo} | {categoria} | {data_str} | {descricao}"
            print(texto)
            linhas_resultado.append(texto)

            # se for saída, conta como gasto
            if tipo == "saida":
                total_saidas += float(valor)
                qtd_saidas += 1

    print("-----------------------------------------------------------")
    linhas_resultado.append("-----------------------------------------------------------")

    if not encontrou:
        msg = "Nenhuma transação encontrada nesse período."
        print(msg)
        return msg

    resumo = f"Total de GASTOS (saídas) no período: R$ {total_saidas:.2f}"
    print(resumo)
    linhas_resultado.append(resumo)

    if qtd_saidas > 0:
        media_gastos = total_saidas / qtd_saidas
        resumo2 = f"MÉDIA de gasto por transação no período: R$ {media_gastos:.2f}"
        print(resumo2)
        linhas_resultado.append(resumo2)
    else:
        resumo2 = "Não houve saídas (gastos) no período, portanto não há média de gastos."
        print(resumo2)
        linhas_resultado.append(resumo2)

    return "\n".join(linhas_resultado)




#------------------------------Opção 5-------------------------------


def calcular_saldo_periodo(ws, data_inicial, data_final):
    """
    data_inicial e data_final são objetos datetime já validados.
    """
    print("\n----------------------------Saldo por período-----------------------------")

    # Verificar se o período é válido
    if data_inicial > data_final:
        msg = "Período inválido: a data inicial é maior que a final."
        print(msg)
        return msg

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

    linhas_resultado = []
    linhas_resultado.append("================== RESULTADO DO PERÍODO ==================")
    cabecalho = f"Período: {data_inicial.strftime('%d/%m/%Y')}  até  {data_final.strftime('%d/%m/%Y')}"
    linhas_resultado.append(cabecalho)
    linhas_resultado.append("----------------------------------------------------------")

    print("\n================== RESULTADO DO PERÍODO ==================")
    print(cabecalho)
    print("----------------------------------------------------------")

    if not encontrou:
        msg = "Nenhuma transação encontrada nesse período."
        print(msg)
        linhas_resultado.append(msg)
        return "\n".join(linhas_resultado)

    # Totais gerais do período
    txt_ent = f"Total de ENTRADAS: R$ {total_entradas:.2f}"
    txt_sai = f"Total de SAÍDAS..: R$ {total_saidas:.2f}"
    txt_saldo = f"SALDO NO PERÍODO.: R$ {saldo:.2f}"

    print(txt_ent)
    print(txt_sai)
    print("----------------------------------------------------------")
    print(txt_saldo)

    linhas_resultado.append(txt_ent)
    linhas_resultado.append(txt_sai)
    linhas_resultado.append("----------------------------------------------------------")
    linhas_resultado.append(txt_saldo)

    # Saldo por mês
    linhas_resultado.append("\n================== SALDO POR MÊS ==================")
    print("\n================== SALDO POR MÊS ==================")

    # ordenar por ano, depois por mês
    chaves_ordenadas = sorted(saldo_por_mes.keys())  # ordena por (ano, mes)

    for (ano_m, mes_m) in chaves_ordenadas:
        saldo_mes = saldo_por_mes[(ano_m, mes_m)]
        linha_mes = f"Mês {mes_m:02d}/{ano_m}: R$ {saldo_mes:.2f}"
        print(linha_mes)
        linhas_resultado.append(linha_mes)

    return "\n".join(linhas_resultado)
