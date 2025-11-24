# Desafio_TheLastCoin

📘 The Last Coin – Sistema de Controle Financeiro com Tkinter, Excel e Gráficos

Este projeto é um sistema de controle financeiro pessoal desenvolvido em Python, com interface gráfica via Tkinter, armazenamento persistente em Excel (openpyxl) e geração de gráficos com Matplotlib.

Ele permite cadastrar usuários, registrar transações financeiras (entradas e saídas), consultar relatórios e visualizar gráficos de gastos.

🚀 Funcionalidades Principais
🔐 1. Cadastro e Login de Usuários

Cadastro de novos usuários.

Login simples usando Tkinter.

Usuários ficam armazenados apenas em memória (não persistem após fechar o app).

💰 2. Registro de Transações

Cada transação inclui:

Valor

Tipo (entrada ou saída)

Categoria (lazer, alimento, trabalho, estudos)

Descrição

Data (dia, mês, ano)

As transações são salvas automaticamente em:

Controle_Financeiro.xlsx

📄 3. Relatórios

O menu financeiro permite:

✔ Listar transações por categoria

Mostra todas as transações pertencentes a uma categoria e calcula:

Total gasto (saídas)

Média de gastos da categoria

✔ Listar transações por período

Com entrada de datas (DD/MM/AAAA), mostra:

Todas as transações dentro do intervalo

Total gasto

Média de gastos

✔ Saldo por período

Exibe:

Total de entradas

Total de saídas

Saldo líquido

Saldo agrupado por mês

📊 4. Visualizações (Gráficos)
🥧 Gráfico de Pizza — Gastos por Categoria

Mostra a proporção das saídas entre:

lazer

alimento

trabalho

estudos

📈 Gráfico de Linha — Saldo Acumulado

Exibe a evolução do saldo ao longo do tempo
(Entradas aumentam o saldo, saídas reduzem).

🧱 Estrutura do Projeto
Desafio_TheLastCoin/
│
├── Cadastro_Coin.py      # Interface gráfica, menus e integração Tkinter
├── Funções_Coin.py       # Todas as funções financeiras e geração de gráficos
├── Controle_Financeiro.xlsx   # Gerado automaticamente na primeira execução
└── README.md

🛠 Tecnologias Utilizadas

Python 3.10+

Tkinter (interface gráfica)

openpyxl (leitura/escrita no Excel)

matplotlib (gráficos)

datetime (manipulação de datas)

▶️ Como Executar
1. Crie o ambiente virtual (opcional)
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

2. Instale as dependências
pip install openpyxl matplotlib

3. Execute o projeto
python Cadastro_Coin.py
