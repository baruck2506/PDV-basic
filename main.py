import tkinter as tk
from tkinter import messagebox, simpledialog
import sqlite3
from datetime import datetime

# ================= Banco de Dados =================
conn = sqlite3.connect("pdv.db")
cursor = conn.cursor()

# Criar tabelas
cursor.execute("""
CREATE TABLE IF NOT EXISTS produtos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT UNIQUE,
    preco REAL,
    estoque INTEGER
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS vendas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    total REAL,
    data TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS itens_venda (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    venda_id INTEGER,
    produto_id INTEGER,
    quantidade INTEGER,
    FOREIGN KEY(venda_id) REFERENCES vendas(id),
    FOREIGN KEY(produto_id) REFERENCES produtos(id)
)
""")
conn.commit()

carrinho = {}

# ================= Funções de Produtos =================
def adicionar_produto_db(nome, preco, estoque):
    try:
        cursor.execute("INSERT INTO produtos (nome, preco, estoque) VALUES (?, ?, ?)", (nome, preco, estoque))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        messagebox.showerror("Erro", "Produto já cadastrado!")
        return False

def remover_produto_db(nome):
    cursor.execute("DELETE FROM produtos WHERE nome=?", (nome,))
    conn.commit()

def alterar_produto_db(nome_atual, novo_nome, novo_preco, novo_estoque):
    cursor.execute("""
        UPDATE produtos
        SET nome=?, preco=?, estoque=?
        WHERE nome=?
    """, (novo_nome, novo_preco, novo_estoque, nome_atual))
    conn.commit()

def listar_produtos_db():
    cursor.execute("SELECT id, nome, preco, estoque FROM produtos")
    return cursor.fetchall()  # Lista de tuplas (id, nome, preco, estoque)

# ================= Janela de Produtos =================
def abrir_janela_produtos():
    janela_produtos = tk.Toplevel()
    janela_produtos.title("Cadastro de Produtos")

    tk.Label(janela_produtos, text="Nome do Produto").pack()
    entry_nome = tk.Entry(janela_produtos)
    entry_nome.pack()

    tk.Label(janela_produtos, text="Preço").pack()
    entry_preco = tk.Entry(janela_produtos)
    entry_preco.pack()

    tk.Label(janela_produtos, text="Estoque").pack()
    entry_estoque = tk.Entry(janela_produtos)
    entry_estoque.pack()

    list_produtos = tk.Listbox(janela_produtos, width=50)
    list_produtos.pack(pady=5)

    def atualizar_lista_produtos():
        list_produtos.delete(0, tk.END)
        for _, nome, preco, estoque in listar_produtos_db():
            list_produtos.insert(tk.END, f"{nome} - R$ {preco:.2f} - Estoque: {estoque}")

    atualizar_lista_produtos()

    def adicionar_produto():
        nome = entry_nome.get()
        preco = entry_preco.get()
        estoque = entry_estoque.get()
        if nome and preco and estoque:
            try:
                preco = float(preco)
                estoque = int(estoque)
                if preco < 0 or estoque < 0:
                    raise ValueError
                if adicionar_produto_db(nome, preco, estoque):
                    atualizar_lista_produtos()
                    entry_nome.delete(0, tk.END)
                    entry_preco.delete(0, tk.END)
                    entry_estoque.delete(0, tk.END)
            except ValueError:
                messagebox.showerror("Erro", "Preço ou estoque inválido!")
        else:
            messagebox.showerror("Erro", "Preencha todos os campos!")

    def remover_produto():
        selecao = list_produtos.curselection()
        if not selecao:
            messagebox.showerror("Erro", "Selecione um produto para remover!")
            return
        item = list_produtos.get(selecao[0])
        nome = item.split(" - ")[0]
        confirmar = messagebox.askyesno("Confirmar", f"Deseja remover o produto '{nome}'?")
        if confirmar:
            remover_produto_db(nome)
            atualizar_lista_produtos()

    def alterar_produto():
        selecao = list_produtos.curselection()
        if not selecao:
            messagebox.showerror("Erro", "Selecione um produto para alterar!")
            return
        item = list_produtos.get(selecao[0])
        nome_atual = item.split(" - ")[0]
        cursor.execute("SELECT preco, estoque FROM produtos WHERE nome=?", (nome_atual,))
        preco_atual, estoque_atual = cursor.fetchone()

        novo_nome = simpledialog.askstring("Alterar Produto", "Novo nome:", initialvalue=nome_atual)
        if not novo_nome:
            return
        try:
            novo_preco = simpledialog.askfloat("Alterar Produto", "Novo preço:", initialvalue=preco_atual, minvalue=0)
            if novo_preco is None:
                return
            novo_estoque = simpledialog.askinteger("Alterar Produto", "Novo estoque:", initialvalue=estoque_atual, minvalue=0)
            if novo_estoque is None:
                return
        except ValueError:
            messagebox.showerror("Erro", "Valores inválidos!")
            return

        alterar_produto_db(nome_atual, novo_nome, novo_preco, novo_estoque)
        atualizar_lista_produtos()

    tk.Button(janela_produtos, text="Adicionar Produto", command=adicionar_produto).pack(pady=5)
    tk.Button(janela_produtos, text="Remover Produto", command=remover_produto).pack(pady=5)
    tk.Button(janela_produtos, text="Alterar Produto", command=alterar_produto).pack(pady=5)

# ================= Janela de Vendas =================
def abrir_janela_vendas():
    janela_vendas = tk.Toplevel()
    janela_vendas.title("Vendas")

    tk.Label(janela_vendas, text="Produtos Disponíveis").pack()
    list_produtos_venda = tk.Listbox(janela_vendas, width=40)
    list_produtos_venda.pack()

    def atualizar_lista_produtos_venda():
        list_produtos_venda.delete(0, tk.END)
        for _, nome, preco, estoque in listar_produtos_db():
            list_produtos_venda.insert(tk.END, f"{nome} - R$ {preco:.2f} - Estoque: {estoque}")

    atualizar_lista_produtos_venda()

    tk.Label(janela_vendas, text="Carrinho").pack()
    list_carrinho_venda = tk.Listbox(janela_vendas, width=40)
    list_carrinho_venda.pack()

    label_total = tk.Label(janela_vendas, text="Total: R$ 0.00", font=("Arial", 14))
    label_total.pack(pady=5)

    # Funções do carrinho
    def atualizar_carrinho():
        list_carrinho_venda.delete(0, tk.END)
        total = 0
        for nome, qtd in carrinho.items():
            cursor.execute("SELECT preco FROM produtos WHERE nome=?", (nome,))
            preco = cursor.fetchone()[0]
            subtotal = preco * qtd
            list_carrinho_venda.insert(tk.END, f"{nome} x{qtd} - R$ {subtotal:.2f}")
            total += subtotal
        label_total.config(text=f"Total: R$ {total:.2f}")

    def adicionar_ao_carrinho():
        selecao = list_produtos_venda.curselection()
        if not selecao:
            messagebox.showerror("Erro", "Selecione um produto!")
            return
        item = list_produtos_venda.get(selecao[0])
        nome = item.split(" - ")[0]

        qtd = simpledialog.askinteger("Quantidade", f"Quantidade de {nome}:", minvalue=1)
        if not qtd:
            return

        if nome in carrinho:
            carrinho[nome] += qtd
        else:
            carrinho[nome] = qtd
        atualizar_carrinho()

    def remover_do_carrinho():
        selecao = list_carrinho_venda.curselection()
        if not selecao:
            messagebox.showerror("Erro", "Selecione um item para remover!")
            return
        item = list_carrinho_venda.get(selecao[0])
        nome = item.split(" x")[0]

        qtd_atual = carrinho[nome]
        if qtd_atual > 1:
            diminuir = simpledialog.askinteger(
                "Remover Item",
                f"Quantidade atual de {nome}: {qtd_atual}\nQuantos deseja remover?",
                minvalue=1, maxvalue=qtd_atual
            )
            if diminuir:
                carrinho[nome] -= diminuir
                if carrinho[nome] <= 0:
                    del carrinho[nome]
        else:
            del carrinho[nome]
        atualizar_carrinho()

    def finalizar_venda():
        if not carrinho:
            messagebox.showerror("Erro", "Carrinho vazio!")
            return

        total_venda = 0
        for nome, qtd in carrinho.items():
            cursor.execute("SELECT id, preco FROM produtos WHERE nome=?", (nome,))
            produto_id, preco = cursor.fetchone()
            subtotal = preco * qtd
            total_venda += subtotal

        # Salvar venda
        data_atual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("INSERT INTO vendas (total, data) VALUES (?, ?)", (total_venda, data_atual))
        venda_id = cursor.lastrowid

        for nome, qtd in carrinho.items():
            cursor.execute("SELECT id FROM produtos WHERE nome=?", (nome,))
            produto_id = cursor.fetchone()[0]
            cursor.execute("INSERT INTO itens_venda (venda_id, produto_id, quantidade) VALUES (?, ?, ?)",
                           (venda_id, produto_id, qtd))
        conn.commit()
        carrinho.clear()
        atualizar_carrinho()
        atualizar_lista_produtos_venda()
        messagebox.showinfo("Sucesso", "Venda finalizada!")

    tk.Button(janela_vendas, text="Adicionar ao Carrinho", command=adicionar_ao_carrinho).pack(pady=5)
    tk.Button(janela_vendas, text="Remover do Carrinho", command=remover_do_carrinho).pack(pady=5)
    tk.Button(janela_vendas, text="Finalizar Venda", command=finalizar_venda).pack(pady=5)

# ================= Janela principal =================
root = tk.Tk()
root.title("PDV Inteligente")

tk.Button(root, text="Abrir Cadastro de Produtos", width=30, command=abrir_janela_produtos).pack(pady=10)
tk.Button(root, text="Abrir Vendas", width=30, command=abrir_janela_vendas).pack(pady=10)

root.mainloop()
