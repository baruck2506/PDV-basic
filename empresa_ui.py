# empresa_ui.py
import tkinter as tk
from tkinter import messagebox
import db

def abrir_janela_empresa():
    janela = tk.Toplevel()
    janela.title("Configuração da Empresa")
    janela.geometry("420x320")
    janela.grab_set()  # janela modal

    # ===== Menubar com atalho =====
    menubar = tk.Menu(janela)
    menu_arquivo = tk.Menu(menubar, tearoff=0)
    # o comando será ligado depois que salvar() existir
    menubar.add_cascade(label="Arquivo", menu=menu_arquivo)
    janela.config(menu=menubar)

    # ===== Campos =====
    lbl_hint = tk.Label(janela, text="Dica: use Ctrl+S para salvar", fg="gray")
    lbl_hint.pack(anchor="w", padx=10, pady=(8, 0))

    tk.Label(janela, text="Nome da Empresa").pack(anchor="w", padx=10, pady=(10, 0))
    entry_nome = tk.Entry(janela, width=50)
    entry_nome.pack(padx=10, pady=2)

    tk.Label(janela, text="CNPJ").pack(anchor="w", padx=10, pady=(10, 0))
    entry_cnpj = tk.Entry(janela, width=50)
    entry_cnpj.pack(padx=10, pady=2)

    tk.Label(janela, text="Endereço").pack(anchor="w", padx=10, pady=(10, 0))
    entry_endereco = tk.Entry(janela, width=50)
    entry_endereco.pack(padx=10, pady=2)

    tk.Label(janela, text="Telefone").pack(anchor="w", padx=10, pady=(10, 0))
    entry_telefone = tk.Entry(janela, width=50)
    entry_telefone.pack(padx=10, pady=2)

    # Carregar dados existentes
    empresa = db.carregar_empresa()
    if empresa:
        nome, cnpj, endereco, telefone = empresa
        entry_nome.insert(0, nome)
        entry_cnpj.insert(0, cnpj)
        entry_endereco.insert(0, endereco)
        entry_telefone.insert(0, telefone)

    # ===== Função salvar (aceita evento do atalho) =====
    def salvar(event=None):
        nome = entry_nome.get().strip()
        cnpj = entry_cnpj.get().strip()
        endereco = entry_endereco.get().strip()
        telefone = entry_telefone.get().strip()

        if not nome or not cnpj or not endereco or not telefone:
            messagebox.showerror("Erro", "Preencha todos os campos!")
            return "break"  # evita beep em alguns sistemas

        db.salvar_empresa(nome, cnpj, endereco, telefone)
        messagebox.showinfo("Sucesso", "Dados da empresa salvos!")
        return "break"

    # Conectar item de menu ao salvar
    menu_arquivo.add_command(label="Salvar    Ctrl+S", command=salvar)

    # ===== Atalhos de teclado =====
    janela.bind("<Control-s>", salvar)   # Ctrl+S salva
    janela.bind("<Return>", salvar)      # Enter salva (se quiser, remova esta linha)
    # Opcional: fechar com Esc
    janela.bind("<Escape>", lambda e: janela.destroy())

    # Foco inicial
    entry_nome.focus_set()

    # Forçar desenho (às vezes ajuda no .exe)
    janela.update_idletasks()
