# vendas_ui.py
import tkinter as tk
from tkinter import messagebox, simpledialog
import db
from datetime import datetime

carrinho = {}

def abrir_janela_vendas(funcionario):
    janela_vendas = tk.Toplevel()
    janela_vendas.title("PDV - Vendas")

    # Lista de produtos
    tk.Label(janela_vendas, text="Produtos Disponíveis").pack()
    list_produtos_venda = tk.Listbox(janela_vendas, width=50)
    list_produtos_venda.pack()

    def atualizar_lista_produtos_venda():
        list_produtos_venda.delete(0, tk.END)
        for _, nome, preco, estoque in db.listar_produtos():
            list_produtos_venda.insert(tk.END, f"{nome} - R$ {preco:.2f} - Estoque: {estoque}")

    atualizar_lista_produtos_venda()

    # Carrinho
    tk.Label(janela_vendas, text="Carrinho").pack()
    list_carrinho_venda = tk.Listbox(janela_vendas, width=50)
    list_carrinho_venda.pack()

    label_total = tk.Label(janela_vendas, text="Total: R$ 0.00", font=("Arial", 14))
    label_total.pack(pady=5)

    # ================= Funções do Carrinho =================
    def atualizar_carrinho():
        list_carrinho_venda.delete(0, tk.END)
        total = 0
        for nome, qtd in carrinho.items():
            cursor = db.cursor
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

    # ================= Finalizar Venda =================
    def finalizar_venda():
        if not carrinho:
            messagebox.showerror("Erro", "Carrinho vazio!")
            return

        db.salvar_venda(carrinho, funcionario)

        # Gerar cupom fiscal
        empresa = db.carregar_empresa()
        data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        total = 0

        nome_arquivo = f"cupom_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(nome_arquivo, "w", encoding="utf-8") as f:
            if empresa:
                f.write(f"{empresa[0]}\nCNPJ: {empresa[1]}\nEndereço: {empresa[2]}\nTelefone: {empresa[3]}\n")
                f.write("="*40 + "\n")
            f.write(f"Funcionario: {funcionario}\nData: {data_hora}\n\n")
            f.write("Produtos:\n")
            f.write(f"{'Nome':20} {'Qtd':>3} {'Preço':>7} {'Subtotal':>10}\n")
            f.write("-"*40 + "\n")
            for nome, qtd in carrinho.items():
                cursor = db.cursor
                cursor.execute("SELECT preco FROM produtos WHERE nome=?", (nome,))
                preco = cursor.fetchone()[0]
                subtotal = preco * qtd
                total += subtotal
                f.write(f"{nome:20} {qtd:>3} R$ {preco:7.2f} R$ {subtotal:10.2f}\n")
            f.write("-"*40 + "\n")
            f.write(f"TOTAL: R$ {total:.2f}\n")
        
        carrinho.clear()
        atualizar_carrinho()
        atualizar_lista_produtos_venda()
        messagebox.showinfo("Sucesso", f"Venda finalizada! Cupom salvo em {nome_arquivo}")

    tk.Button(janela_vendas, text="Adicionar ao Carrinho", command=adicionar_ao_carrinho).pack(pady=5)
    tk.Button(janela_vendas, text="Remover do Carrinho", command=remover_do_carrinho).pack(pady=5)
    tk.Button(janela_vendas, text="Finalizar Venda", command=finalizar_venda).pack(pady=5)
