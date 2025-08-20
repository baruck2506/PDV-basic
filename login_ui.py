# login_ui.py
import tkinter as tk
from tkinter import messagebox
import db

def abrir_login(root, on_success):
    login_janela = tk.Toplevel(root)
    login_janela.title("Login")

    tk.Label(login_janela, text="Usuário").pack(pady=5)
    entry_usuario = tk.Entry(login_janela)
    entry_usuario.pack(pady=5)

    tk.Label(login_janela, text="Senha").pack(pady=5)
    entry_senha = tk.Entry(login_janela, show="*")
    entry_senha.pack(pady=5)

    def tentar_login():
        username = entry_usuario.get()
        senha = entry_senha.get()
        tipo = db.autenticar_usuario(username, senha)
        if tipo:
            login_janela.destroy()
            # Passa tipo e o nome do usuário logado
            on_success(tipo, username)
        else:
            messagebox.showerror("Erro", "Usuário ou senha inválidos!")

    tk.Button(login_janela, text="Entrar", command=tentar_login).pack(pady=10)
    
    # Permite fechar a janela de login corretamente
    def sair_app():
        db.fechar_conexao()
        login_janela.destroy()
        root.destroy()  # garante que o loop principal encerre

    login_janela.protocol("WM_DELETE_WINDOW", sair_app)
