from datetime import datetime
from Funções_Coin import (
    criar_planilha,
    adicionar_transa,          # continua existindo, mas não é mais chamado pelo Tk
    remover_transa,
    calcular_saldo_periodo,
    listar_por_categoria,
    listar_por_periodo,
    grafico_pizza_categorias,
    grafico_saldo_acumulado,
)

import tkinter as tk
from tkinter import messagebox

usuarios = {}
root = None


def mostrar_texto(titulo, conteudo):
    if not conteudo:
        messagebox.showinfo(titulo, "Nenhum dado para exibir.")
        return

    janela_txt = tk.Toplevel(root)
    janela_txt.title(titulo)
    janela_txt.geometry("650x400")

    txt = tk.Text(janela_txt, wrap="word")
    txt.pack(fill="both", expand=True)

    txt.insert("1.0", conteudo)
    txt.config(state="disabled")


# ------------------------ JANELAS AUXILIARES DO MENU FINANCEIRO ------------------------


def gui_remover_transacao(wb, ws):

    # Verifica se há transações
    linhas = list(ws.iter_rows(min_row=2, values_only=True))
    if not linhas:
        messagebox.showinfo("Remover transação", "Não há transações cadastradas.")
        return

    def confirmar_remocao():
        id_str = entry_id.get().strip()
        if not id_str.isdigit():
            messagebox.showerror("Erro", "ID deve ser um número inteiro.")
            return
        id_rem = int(id_str)
        ok, detalhes = remover_transa(wb, ws, id_rem)
        if ok:
            messagebox.showinfo("Sucesso", "Transação removida:\n\n" + detalhes)
            janela.destroy()
        else:
            messagebox.showerror("Erro", detalhes)

    janela = tk.Toplevel(root)
    janela.title("Remover transação")
    janela.geometry("650x400")

    tk.Label(janela, text="Transações cadastradas:").pack(pady=(10, 5))

    txt = tk.Text(janela, height=15, wrap="none")
    txt.pack(fill="both", expand=True)

    txt.insert("1.0", "ID | Valor | Tipo | Categoria | Data       | Descrição\n")
    txt.insert("end", "-----------------------------------------------------------\n")

    for linha in linhas:
        tid, valor, tipo, categoria, descricao, dia, mes, ano = linha
        data_str = f"{int(dia):02d}/{int(mes):02d}/{int(ano)}"
        txt.insert("end", f"{tid} | {valor} | {tipo} | {categoria} | {data_str} | {descricao}\n")

    txt.config(state="disabled")

    frame_id = tk.Frame(janela)
    frame_id.pack(pady=10)

    tk.Label(frame_id, text="ID a remover:").pack(side="left", padx=5)
    entry_id = tk.Entry(frame_id, width=10)
    entry_id.pack(side="left")

    tk.Button(janela, text="Remover", command=confirmar_remocao).pack(pady=5)


def gui_listar_categoria(ws):

    def confirmar():
        cat = entry_cat.get().strip().lower()
        if cat == "":
            messagebox.showerror("Erro", "Informe uma categoria.")
            return
        resultado = listar_por_categoria(ws, cat)
        mostrar_texto("Transações por categoria", resultado)
        janela.destroy()

    janela = tk.Toplevel(root)
    janela.title("Listar por categoria")
    janela.geometry("300x140")

    tk.Label(janela, text="Categoria (lazer, alimento, trabalho, estudos):").pack(pady=(10, 5))
    entry_cat = tk.Entry(janela)
    entry_cat.pack()

    tk.Button(janela, text="Listar", command=confirmar).pack(pady=10)


def gui_listar_periodo(ws):

    def confirmar():
        d1_str = entry_ini.get().strip()
        d2_str = entry_fim.get().strip()
        if d1_str == "" or d2_str == "":
            messagebox.showerror("Erro", "Preencha as duas datas.")
            return

        try:
            data_inicial = datetime.strptime(d1_str, "%d/%m/%Y")
            data_final = datetime.strptime(d2_str, "%d/%m/%Y")
        except ValueError:
            messagebox.showerror("Erro", "Data inválida. Use o formato DD/MM/AAAA.")
            return

        resultado = listar_por_periodo(ws, data_inicial, data_final)
        mostrar_texto("Transações por período", resultado)
        janela.destroy()

    janela = tk.Toplevel(root)
    janela.title("Listar por período")
    janela.geometry("300x170")

    tk.Label(janela, text="Data inicial (DD/MM/AAAA):").pack(pady=(10, 0))
    entry_ini = tk.Entry(janela)
    entry_ini.pack()

    tk.Label(janela, text="Data final (DD/MM/AAAA):").pack(pady=(10, 0))
    entry_fim = tk.Entry(janela)
    entry_fim.pack()

    tk.Button(janela, text="Listar", command=confirmar).pack(pady=10)


def gui_saldo_periodo(ws):
    """Abre janela para pedir período e calcular saldo."""

    def confirmar():
        d1_str = entry_ini.get().strip()
        d2_str = entry_fim.get().strip()
        if d1_str == "" or d2_str == "":
            messagebox.showerror("Erro", "Preencha as duas datas.")
            return

        try:
            data_inicial = datetime.strptime(d1_str, "%d/%m/%Y")
            data_final = datetime.strptime(d2_str, "%d/%m/%Y")
        except ValueError:
            messagebox.showerror("Erro", "Data inválida. Use o formato DD/MM/AAAA.")
            return

        resultado = calcular_saldo_periodo(ws, data_inicial, data_final)
        mostrar_texto("Saldo por período", resultado)
        janela.destroy()

    janela = tk.Toplevel(root)
    janela.title("Saldo por período")
    janela.geometry("300x170")

    tk.Label(janela, text="Data inicial (DD/MM/AAAA):").pack(pady=(10, 0))
    entry_ini = tk.Entry(janela)
    entry_ini.pack()

    tk.Label(janela, text="Data final (DD/MM/AAAA):").pack(pady=(10, 0))
    entry_fim = tk.Entry(janela)
    entry_fim.pack()

    tk.Button(janela, text="Calcular", command=confirmar).pack(pady=10)


# ------------------------ NOVA JANELA: ADICIONAR TRANSAÇÃO (GUI) ------------------------


def gui_adicionar_transacao(wb, ws):
    """Janela Tkinter para cadastrar UMA transação, sem usar o terminal."""

    def salvar():
        # VALOR
        valor_str = entry_valor.get().strip().replace(",", ".")
        try:
            valor = float(valor_str)
            if valor <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Erro", "Valor inválido. Informe um número maior que zero.")
            return

        # TIPO (entrada/saida)
        tipo = var_tipo.get()
        if tipo not in ["entrada", "saida"]:
            messagebox.showerror("Erro", "Selecione o tipo de transação.")
            return

        # CATEGORIA
        categoria = var_cat.get().strip().lower()
        if categoria not in ["lazer", "alimento", "trabalho", "estudos"]:
            messagebox.showerror("Erro", "Categoria inválida.")
            return

        # DESCRIÇÃO
        descricao = entry_desc.get().strip()
        if descricao == "":
            messagebox.showerror("Erro", "Descrição não pode ser vazia.")
            return

        # DIA / MÊS / ANO
        try:
            dia = int(entry_dia.get().strip())
            mes = int(entry_mes.get().strip())
            ano = int(entry_ano.get().strip())
        except ValueError:
            messagebox.showerror("Erro", "Dia, mês e ano devem ser números inteiros.")
            return

        if not (1 <= dia <= 31):
            messagebox.showerror("Erro", "Dia deve estar entre 1 e 31.")
            return
        if not (1 <= mes <= 12):
            messagebox.showerror("Erro", "Mês deve estar entre 1 e 12.")
            return
        if not (1 <= ano <= 9999):
            messagebox.showerror("Erro", "Ano deve estar entre 1 e 9999.")
            return

        # validação de data real (evita 31/02, etc.)
        try:
            datetime(ano, mes, dia)
        except ValueError:
            messagebox.showerror("Erro", "Data inválida.")
            return

        # Descobrir o próximo ID
        max_id = 0
        for linha in ws.iter_rows(min_row=2, max_col=1, values_only=True):
            cell_id = linha[0]
            if cell_id is None:
                continue
            try:
                iid = int(cell_id)
                if iid > max_id:
                    max_id = iid
            except Exception:
                continue

        id_transacao = max_id + 1

        # Salvar na planilha
        ws.append([id_transacao, valor, tipo, categoria, descricao, dia, mes, ano])
        wb.save("Controle_Financeiro.xlsx")

        messagebox.showinfo("Sucesso", f"Transação {id_transacao} salva com sucesso!")
        janela.destroy()

    janela = tk.Toplevel(root)
    janela.title("Adicionar transação")
    janela.geometry("320x380")

    # Valor
    tk.Label(janela, text="Valor:").pack(pady=(10, 0))
    entry_valor = tk.Entry(janela)
    entry_valor.pack()

    # Tipo
    tk.Label(janela, text="Tipo:").pack(pady=(10, 0))
    var_tipo = tk.StringVar(value="entrada")
    frame_tipo = tk.Frame(janela)
    frame_tipo.pack()
    tk.Radiobutton(frame_tipo, text="Entrada", variable=var_tipo, value="entrada").pack(side="left", padx=5)
    tk.Radiobutton(frame_tipo, text="Saída", variable=var_tipo, value="saida").pack(side="left", padx=5)

    # Categoria
    tk.Label(janela, text="Categoria:").pack(pady=(10, 0))
    categorias = ["lazer", "alimento", "trabalho", "estudos"]
    var_cat = tk.StringVar(value=categorias[0])
    opt_cat = tk.OptionMenu(janela, var_cat, *categorias)
    opt_cat.pack()

    # Descrição
    tk.Label(janela, text="Descrição:").pack(pady=(10, 0))
    entry_desc = tk.Entry(janela)
    entry_desc.pack()

    # Data
    frame_data = tk.Frame(janela)
    frame_data.pack(pady=10)

    tk.Label(frame_data, text="Dia:").grid(row=0, column=0, padx=2)
    entry_dia = tk.Entry(frame_data, width=4)
    entry_dia.grid(row=0, column=1, padx=2)

    tk.Label(frame_data, text="Mês:").grid(row=0, column=2, padx=2)
    entry_mes = tk.Entry(frame_data, width=4)
    entry_mes.grid(row=0, column=3, padx=2)

    tk.Label(frame_data, text="Ano:").grid(row=0, column=4, padx=2)
    entry_ano = tk.Entry(frame_data, width=6)
    entry_ano.grid(row=0, column=5, padx=2)

    tk.Button(janela, text="Salvar transação", command=salvar).pack(pady=15)


# ------------------------ VISUALIZAÇÕES (GRÁFICOS) ------------------------


def abrir_menu_visualizacoes(ws):
    """Janela com as opções de gráficos (pizza e linha)."""

    def chamar_pizza():
        msg = grafico_pizza_categorias(ws)
        if msg:
            messagebox.showinfo("Visualizações", msg)

    def chamar_linha():
        msg = grafico_saldo_acumulado(ws)
        if msg:
            messagebox.showinfo("Visualizações", msg)

    janela_vis = tk.Toplevel(root)
    janela_vis.title("Visualizações")
    janela_vis.geometry("320x180")

    tk.Label(janela_vis, text="Escolha o tipo de gráfico:").pack(pady=10)

    tk.Button(
        janela_vis,
        text="Gráfico de pizza (gastos por categoria)",
        wraplength=260,
        command=chamar_pizza
    ).pack(pady=5)

    tk.Button(
        janela_vis,
        text="Gráfico de linha (saldo acumulado)",
        wraplength=260,
        command=chamar_linha
    ).pack(pady=5)


# ------------------------ CADASTRO / LOGIN ------------------------


def cadastrar_usuario_tk():
    def salvar_usuario():
        nome = entry_nome.get().strip()
        senha = entry_senha.get().strip()

        if nome == "":
            messagebox.showerror("Erro", "Nome de usuário não pode ser vazio.")
            return
        if nome in usuarios:
            messagebox.showerror("Erro", "Usuário já existe. Tente outro nome.")
            return
        if senha == "":
            messagebox.showerror("Erro", "Senha não pode ser vazia.")
            return

        usuarios[nome] = senha
        messagebox.showinfo("Sucesso", f"Usuário '{nome}' cadastrado com sucesso!")
        janela.destroy()

    janela = tk.Toplevel(root)
    janela.title("Cadastro de Usuário")
    janela.geometry("300x160")

    tk.Label(janela, text="Nome de usuário:").pack(pady=(10, 0))
    entry_nome = tk.Entry(janela)
    entry_nome.pack()

    tk.Label(janela, text="Senha:").pack(pady=(10, 0))
    entry_senha = tk.Entry(janela, show="*")
    entry_senha.pack()

    tk.Button(janela, text="Cadastrar", command=salvar_usuario).pack(pady=15)


def fazer_login_tk():
    def tentar_login():
        nome = entry_nome.get().strip()
        senha = entry_senha.get().strip()

        if nome in usuarios and usuarios[nome] == senha:
            messagebox.showinfo("Sucesso", f"Login bem-sucedido! Bem-vindo, {nome}.")
            janela_login.destroy()
            abrir_menu_financeiro(nome)
        else:
            messagebox.showerror("Erro", "Usuário ou senha inválidos.")

    janela_login = tk.Toplevel(root)
    janela_login.title("Login")
    janela_login.geometry("300x160")

    tk.Label(janela_login, text="Usuário:").pack(pady=(10, 0))
    entry_nome = tk.Entry(janela_login)
    entry_nome.pack()

    tk.Label(janela_login, text="Senha:").pack(pady=(10, 0))
    entry_senha = tk.Entry(janela_login, show="*")
    entry_senha.pack()

    tk.Button(janela_login, text="Entrar", command=tentar_login).pack(pady=15)


# ------------------------ MENU FINANCEIRO ------------------------


def abrir_menu_financeiro(usuario_logado):
    wb, ws = criar_planilha()  # abre ou cria o arquivo permanente

    janela_fin = tk.Toplevel(root)
    janela_fin.title(f"Menu Financeiro - {usuario_logado}")
    janela_fin.geometry("300x340")

    tk.Label(janela_fin, text=f"Menu Financeiro ({usuario_logado})").pack(pady=10)

    tk.Button(
        janela_fin,
        text="Adicionar transação",
        width=25,
        command=lambda: gui_adicionar_transacao(wb, ws)  # <- AGORA USA A VERSÃO GUI
    ).pack(pady=3)

    tk.Button(
        janela_fin,
        text="Remover transação",
        width=25,
        command=lambda: gui_remover_transacao(wb, ws)
    ).pack(pady=3)

    tk.Button(
        janela_fin,
        text="Listar por categoria",
        width=25,
        command=lambda: gui_listar_categoria(ws)
    ).pack(pady=3)

    tk.Button(
        janela_fin,
        text="Listar por período",
        width=25,
        command=lambda: gui_listar_periodo(ws)
    ).pack(pady=3)

    tk.Button(
        janela_fin,
        text="Saldo por período",
        width=25,
        command=lambda: gui_saldo_periodo(ws)
    ).pack(pady=3)

    tk.Button(
        janela_fin,
        text="Visualizações",
        width=25,
        command=lambda: abrir_menu_visualizacoes(ws)
    ).pack(pady=3)

    tk.Button(
        janela_fin,
        text="Fechar menu financeiro",
        width=25,
        command=janela_fin.destroy
    ).pack(pady=10)


# ------------------------ MENU INICIAL ------------------------


def menu_inicial():
    global root
    root = tk.Tk()
    root.title("Sistema de Usuários - Coin")
    root.geometry("300x220")

    tk.Label(root, text="Sistema de Controle Financeiro", font=("Arial", 10, "bold")).pack(pady=10)

    tk.Button(root, text="Cadastro", width=20, command=cadastrar_usuario_tk).pack(pady=5)
    tk.Button(root, text="Login", width=20, command=fazer_login_tk).pack(pady=5)
    tk.Button(root, text="Sair", width=20, command=root.destroy).pack(pady=20)

    root.mainloop()


# ------------------ INÍCIO DO PROGRAMA ------------------

if __name__ == "__main__":
    menu_inicial()
