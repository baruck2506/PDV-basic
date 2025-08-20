# login_ui.py
import tkinter as tk
from tkinter import messagebox
import db

def abrir_login(root, on_success):
    login_janela = tk.Toplevel(root)
    login_janela.title("Login")

    tk.Label(login_janela, text="Usuário").pack()
    entry_usuario = tk.Entry(login_janela)
    entry_usuario.pack()

    tk.Label(login_janela, text="Senha").pack()
    entry_senha = tk.Entry(login_janela, show="*")
    entry_senha.pack()

    def tentar_login():
        username = entry_usuario.get()
        senha = entry_senha.get()
        tipo = db.autenticar_usuario(username, senha)
        if tipo:
            login_janela.destroy()
            on_success(tipo)
        else:
            messagebox.showerror("Erro", "Usuário ou senha inválidos!")

    tk.Button(login_janela, text="Entrar", command=tentar_login).pack(pady=10)
    
    def sair_app():
        db.fechar_conexao()
        login_janela.destroy()
        root.destroy()

    login_janela.protocol("WM_DELETE_WINDOW", sair_app)

