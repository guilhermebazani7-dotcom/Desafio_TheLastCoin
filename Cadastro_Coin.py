from datetime import datetime
import logging
from Funções_Coin import (
    criar_planilha,
    adicionar_transa,
    remover_transa,
    calcular_saldo_periodo,
    listar_por_categoria,
    listar_por_periodo,
    grafico_pizza_categorias,
    grafico_saldo_acumulado,
)

import tkinter as tk
from tkinter import messagebox

# ------------------------ LOGGING ------------------------
logging.basicConfig(
    filename="coin_system.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

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
    logging.info("Ação: abrir janela de remover transação")

    linhas = list(ws.iter_rows(min_row=2, values_only=True))
    if not linhas:
        messagebox.showinfo("Remover transação", "Não há transações cadastradas.")
        logging.warning("Tentativa de remover transação sem dados existentes")
        return

    def confirmar_remocao():
        id_str = entry_id.get().strip()
        if not id_str.isdigit():
            messagebox.showerror("Erro", "ID deve ser um número inteiro.")
            return

        id_rem = int(id_str)
        ok, detalhes = remover_transa(wb, ws, id_rem)

        if ok:
            logging.info(f"Transação removida ID={id_rem}")
            messagebox.showinfo("Sucesso", "Transação removida:\n\n" + detalhes)
            janela.destroy()
        else:
            logging.warning(f"Falha ao remover transação ID={id_rem}")
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
    logging.info("Ação: abrir janela listar por categoria")

    def confirmar():
        cat = entry_cat.get().strip().lower()
        if cat == "":
            messagebox.showerror("Erro", "Informe uma categoria.")
            return

        logging.info(f"Listando categoria: {cat}")
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
    logging.info("Ação: abrir janela listar por período")

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

        logging.info(f"Listagem período de {d1_str} até {d2_str}")
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
    logging.info("Ação: abrir janela saldo por período")

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

        logging.info(f"Calculando saldo do período {d1_str} até {d2_str}")
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


# ------------------------ ADICIONAR TRANSAÇÃO ------------------------

def gui_adicionar_transacao(wb, ws):
    logging.info("Ação: abrir janela adicionar transação")

    def salvar():
        valor_str = entry_valor.get().strip().replace(",", ".")
        try:
            valor = float(valor_str)
            if valor <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Erro", "Valor inválido.")
            return

        tipo = var_tipo.get()
        categoria = var_cat.get().strip().lower()
        descricao = entry_desc.get().strip()

        try:
            dia = int(entry_dia.get().strip())
            mes = int(entry_mes.get().strip())
            ano = int(entry_ano.get().strip())
            datetime(ano, mes, dia)
        except:
            messagebox.showerror("Erro", "Data inválida.")
            return

        max_id = 0
        for linha in ws.iter_rows(min_row=2, max_col=1, values_only=True):
            if linha[0] and int(linha[0]) > max_id:
                max_id = int(linha[0])

        id_transacao = max_id + 1

        ws.append([id_transacao, valor, tipo, categoria, descricao, dia, mes, ano])
        wb.save("Controle_Financeiro.xlsx")

        logging.info(f"Transação adicionada ID={id_transacao}, tipo={tipo}, valor={valor}")
        messagebox.showinfo("Sucesso", f"Transação {id_transacao} salva com sucesso!")
        janela.destroy()

    janela = tk.Toplevel(root)
    janela.title("Adicionar transação")
    janela.geometry("320x380")

    tk.Label(janela, text="Valor:").pack(pady=(10, 0))
    entry_valor = tk.Entry(janela)
    entry_valor.pack()

    tk.Label(janela, text="Tipo:").pack(pady=(10, 0))
    var_tipo = tk.StringVar(value="entrada")
    frame_tipo = tk.Frame(janela)
    frame_tipo.pack()
    tk.Radiobutton(frame_tipo, text="Entrada", variable=var_tipo, value="entrada").pack(side="left", padx=5)
    tk.Radiobutton(frame_tipo, text="Saída", variable=var_tipo, value="saida").pack(side="left", padx=5)

    tk.Label(janela, text="Categoria:").pack(pady=(10, 0))
    categorias = ["lazer", "alimento", "trabalho", "estudos"]
    var_cat = tk.StringVar(value=categorias[0])
    tk.OptionMenu(janela, var_cat, *categorias).pack()

    tk.Label(janela, text="Descrição:").pack(pady=(10, 0))
    entry_desc = tk.Entry(janela)
    entry_desc.pack()

    frame_data = tk.Frame(janela)
    frame_data.pack(pady=10)

    tk.Label(frame_data, text="Dia:").grid(row=0, column=0)
    entry_dia = tk.Entry(frame_data, width=4)
    entry_dia.grid(row=0, column=1)

    tk.Label(frame_data, text="Mês:").grid(row=0, column=2)
    entry_mes = tk.Entry(frame_data, width=4)
    entry_mes.grid(row=0, column=3)

    tk.Label(frame_data, text="Ano:").grid(row=0, column=4)
    entry_ano = tk.Entry(frame_data, width=6)
    entry_ano.grid(row=0, column=5)

    tk.Button(janela, text="Salvar transação", command=salvar).pack(pady=15)


# ------------------------ VISUALIZAÇÕES ------------------------

def abrir_menu_visualizacoes(ws):
    logging.info("Ação: abrir menu de visualizações")

    def chamar_pizza():
        logging.info("Gerando gráfico de pizza")
        msg = grafico_pizza_categorias(ws)
        messagebox.showinfo("Visualizações", msg)

    def chamar_linha():
        logging.info("Gerando gráfico de linha")
        msg = grafico_saldo_acumulado(ws)
        messagebox.showinfo("Visualizações", msg)

    janela_vis = tk.Toplevel(root)
    janela_vis.title("Visualizações")
    janela_vis.geometry("320x180")

    tk.Label(janela_vis, text="Escolha o tipo de gráfico:").pack(pady=10)

    tk.Button(janela_vis, text="Gráfico de pizza", wraplength=260, command=chamar_pizza).pack(pady=5)
    tk.Button(janela_vis, text="Gráfico de linha", wraplength=260, command=chamar_linha).pack(pady=5)


# ------------------------ CADASTRO / LOGIN ------------------------

def cadastrar_usuario_tk():
    logging.info("Ação: janela cadastro de usuário")

    def salvar_usuario():
        nome = entry_nome.get().strip()
        senha = entry_senha.get().strip()

        if nome == "" or senha == "":
            messagebox.showerror("Erro", "Preencha todos os campos.")
            return

        if nome in usuarios:
            messagebox.showerror("Erro", "Usuário já existe.")
            logging.warning(f"Cadastro falhou: usuário existente ({nome})")
            return

        usuarios[nome] = senha
        messagebox.showinfo("Sucesso", f"Usuário '{nome}' cadastrado.")
        logging.info(f"Usuário cadastrado: {nome}")
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
    logging.info("Ação: janela login")

    def tentar_login():
        nome = entry_nome.get().strip()
        senha = entry_senha.get().strip()

        if nome in usuarios and usuarios[nome] == senha:
            logging.info(f"Login bem-sucedido: {nome}")
            messagebox.showinfo("Sucesso", f"Login bem-sucedido! Bem-vindo, {nome}.")
            janela_login.destroy()
            abrir_menu_financeiro(nome)
        else:
            logging.warning(f"TENTATIVA DE LOGIN FALHA: {nome}")
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
    logging.info(f"Abrindo menu financeiro do usuário: {usuario_logado}")

    wb, ws = criar_planilha()

    janela_fin = tk.Toplevel(root)
    janela_fin.title(f"Menu Financeiro - {usuario_logado}")
    janela_fin.geometry("300x340")

    tk.Label(janela_fin, text=f"Menu Financeiro ({usuario_logado})").pack(pady=10)

    tk.Button(janela_fin, text="Adicionar transação", width=25,
              command=lambda: gui_adicionar_transacao(wb, ws)).pack(pady=3)

    tk.Button(janela_fin, text="Remover transação", width=25,
              command=lambda: gui_remover_transacao(wb, ws)).pack(pady=3)

    tk.Button(janela_fin, text="Listar por categoria", width=25,
              command=lambda: gui_listar_categoria(ws)).pack(pady=3)

    tk.Button(janela_fin, text="Listar por período", width=25,
              command=lambda: gui_listar_periodo(ws)).pack(pady=3)

    tk.Button(janela_fin, text="Saldo por período", width=25,
              command=lambda: gui_saldo_periodo(ws)).pack(pady=3)

    tk.Button(janela_fin, text="Visualizações", width=25,
              command=lambda: abrir_menu_visualizacoes(ws)).pack(pady=3)

    tk.Button(janela_fin, text="Fechar menu financeiro", width=25,
              command=janela_fin.destroy).pack(pady=10)


# ------------------------ MENU INICIAL ------------------------

def menu_inicial():
    global root
    logging.info("Sistema iniciado")

    root = tk.Tk()
    root.title("Sistema de Usuários - Coin")
    root.geometry("300x220")

    tk.Label(root, text="Sistema de Controle Financeiro",
             font=("Arial", 10, "bold")).pack(pady=10)

    tk.Button(root, text="Cadastro", width=20, command=cadastrar_usuario_tk).pack(pady=5)
    tk.Button(root, text="Login", width=20, command=fazer_login_tk).pack(pady=5)
    tk.Button(root, text="Sair", width=20, command=root.destroy).pack(pady=20)

    root.mainloop()


# ------------------ INÍCIO DO PROGRAMA ------------------

if __name__ == "__main__":
    menu_inicial()
