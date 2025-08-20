# main.py
import tkinter as tk
import produtos_ui
import vendas_ui
import db

db.criar_tabelas()  # garante que o banco e tabelas existam

root = tk.Tk()
root.title("PDV Inteligente")

tk.Button(root, text="Gerenciar Produtos", width=30, command=produtos_ui.abrir_janela_produtos).pack(pady=10)
tk.Button(root, text="Abrir PDV (Vendas)", width=30, command=vendas_ui.abrir_janela_vendas).pack(pady=10)

root.mainloop()
