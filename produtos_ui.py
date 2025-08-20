# produtos_ui.py
import tkinter as tk
from tkinter import messagebox, simpledialog
import db

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
        for _, nome, preco, estoque in db.listar_produtos():
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
                if db.adicionar_produto(nome, preco, estoque):
                    atualizar_lista_produtos()
                    entry_nome.delete(0, tk.END)
                    entry_preco.delete(0, tk.END)
                    entry_estoque.delete(0, tk.END)
                else:
                    messagebox.showerror("Erro", "Produto já cadastrado!")
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
            db.remover_produto(nome)
            atualizar_lista_produtos()

    def alterar_produto():
        selecao = list_produtos.curselection()
        if not selecao:
            messagebox.showerror("Erro", "Selecione um produto para alterar!")
            return
        item = list_produtos.get(selecao[0])
        nome_atual = item.split(" - ")[0]
        _, _, preco_atual, estoque_atual = next(p for p in db.listar_produtos() if p[1] == nome_atual)

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

        db.alterar_produto(nome_atual, novo_nome, novo_preco, novo_estoque)
        atualizar_lista_produtos()

    tk.Button(janela_produtos, text="Adicionar Produto", command=adicionar_produto).pack(pady=5)
    tk.Button(janela_produtos, text="Remover Produto", command=remover_produto).pack(pady=5)
    tk.Button(janela_produtos, text="Alterar Produto", command=alterar_produto).pack(pady=5)
