# vendas_ui.py
import tkinter as tk
from tkinter import messagebox, simpledialog
import db

carrinho = {}

def abrir_janela_vendas():
    janela_vendas = tk.Toplevel()
    janela_vendas.title("Vendas")

    tk.Label(janela_vendas, text="Produtos Disponíveis").pack()
    list_produtos_venda = tk.Listbox(janela_vendas, width=50)
    list_produtos_venda.pack()

    def atualizar_lista_produtos_venda():
        list_produtos_venda.delete(0, tk.END)
        for _, nome, preco, estoque in db.listar_produtos():
            list_produtos_venda.insert(tk.END, f"{nome} - R$ {preco:.2f} - Estoque: {estoque}")

    atualizar_lista_produtos_venda()

    tk.Label(janela_vendas, text="Carrinho").pack()
    list_carrinho_venda = tk.Listbox(janela_vendas, width=50)
    list_carrinho_venda.pack()

    label_total = tk.Label(janela_vendas, text="Total: R$ 0.00", font=("Arial", 14))
    label_total.pack(pady=5)

    def atualizar_carrinho():
        list_carrinho_venda.delete(0, tk.END)
        total = 0
        for nome, qtd in carrinho.items():
            produto = next(p for p in db.listar_produtos() if p[1] == nome)
            preco = produto[2]
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
        db.salvar_venda(carrinho)
        carrinho.clear()
        atualizar_carrinho()
        atualizar_lista_produtos_venda()
        messagebox.showinfo("Sucesso", "Venda finalizada!")

    tk.Button(janela_vendas, text="Adicionar ao Carrinho", command=adicionar_ao_carrinho).pack(pady=5)
    tk.Button(janela_vendas, text="Remover do Carrinho", command=remover_do_carrinho).pack(pady=5)
    tk.Button(janela_vendas, text="Finalizar Venda", command=finalizar_venda).pack(pady=5)
