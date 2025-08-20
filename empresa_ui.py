# empresa_ui.py
import tkinter as tk
from tkinter import messagebox
import db

def abrir_janela_empresa():
    janela = tk.Toplevel()
    janela.title("Configuração da Empresa")
    janela.geometry("400x250")
    janela.grab_set()  # torna a janela modal

    # Labels e Entrys
    tk.Label(janela, text="Nome da Empresa").pack(anchor="w", padx=10, pady=(10, 0))
    entry_nome = tk.Entry(janela, width=50)
    entry_nome.pack(padx=10)

    tk.Label(janela, text="CNPJ").pack(anchor="w", padx=10, pady=(10, 0))
    entry_cnpj = tk.Entry(janela, width=50)
    entry_cnpj.pack(padx=10)

    tk.Label(janela, text="Endereço").pack(anchor="w", padx=10, pady=(10, 0))
    entry_endereco = tk.Entry(janela, width=50)
    entry_endereco.pack(padx=10)

    tk.Label(janela, text="Telefone").pack(anchor="w", padx=10, pady=(10, 0))
    entry_telefone = tk.Entry(janela, width=50)
    entry_telefone.pack(padx=10)

    # Carregar dados existentes
    empresa = db.carregar_empresa()
    if empresa:
        nome, cnpj, endereco, telefone = empresa
        entry_nome.insert(0, nome)
        entry_cnpj.insert(0, cnpj)
        entry_endereco.insert(0, endereco)
        entry_telefone.insert(0, telefone)

    # Função de salvar
    def salvar():
        nome = entry_nome.get().strip()
        cnpj = entry_cnpj.get().strip()
        endereco = entry_endereco.get().strip()
        telefone = entry_telefone.get().strip()

        if not nome or not cnpj or not endereco or not telefone:
            messagebox.showerror("Erro", "Preencha todos os campos!")
            return

        db.salvar_empresa(nome, cnpj, endereco, telefone)
        messagebox.showinfo("Sucesso", "Dados da empresa salvos!")

    # Botão Salvar
    tk.Button(janela, text="Salvar", width=15, command=salvar).pack(pady=15)
