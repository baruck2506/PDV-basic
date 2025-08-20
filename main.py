# main.py
import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import db
import produtos_ui
import vendas_ui
import usuarios_ui
import empresa_ui
import login_ui

# ================= Inicialização do banco =================
db.criar_tabelas()
db.criar_tabela_usuarios()  # garante que a tabela de usuários exista

# Usuários de teste
db.adicionar_usuario("proprietario", "12345", "proprietario")
db.adicionar_usuario("admin", "1234", "admin")
db.adicionar_usuario("funcionario", "1234", "funcionario")


# ================= Funções =================
def gerar_relatorio_diario():
    hoje = datetime.now().strftime("%Y-%m-%d")
    vendas = db.listar_vendas_por_data(hoje)
    if not vendas:
        return  # sem vendas hoje

    nome_arquivo = f"relatorio_{hoje}.txt"
    with open(nome_arquivo, "w", encoding="utf-8") as f:
        f.write(f"Relatório de Vendas - {hoje}\n")
        f.write("="*40 + "\n\n")
        for venda in vendas:
            f.write(f"Data: {venda['data']} - Funcionário: {venda['funcionario']}\n")
            f.write("Itens:\n")
            for item in venda['itens']:
                f.write(f"  {item['nome']} x{item['quantidade']} - R$ {item['preco']:.2f} - Subtotal: R$ {item['subtotal']:.2f}\n")
            f.write(f"Total: R$ {venda['total']:.2f}\n")
            f.write("-"*40 + "\n")
    return nome_arquivo


def abrir_sistema(tipo_usuario, usuario_logado):
    root_frame = tk.Toplevel()
    root_frame.title("PDV Inteligente")

    if tipo_usuario == "proprietario":
        tk.Button(root_frame, text="Gerenciar Usuários", width=30,
                  command=usuarios_ui.abrir_janela_usuarios).pack(pady=5)
        tk.Button(root_frame, text="Gerenciar Produtos", width=30,
                  command=produtos_ui.abrir_janela_produtos).pack(pady=5)
        tk.Button(root_frame, text="Configurar Empresa", width=30,
                  command=empresa_ui.abrir_janela_empresa).pack(pady=5)

    elif tipo_usuario == "admin":
        tk.Button(root_frame, text="Gerenciar Produtos", width=30,
                  command=produtos_ui.abrir_janela_produtos).pack(pady=5)

    # Todos podem acessar vendas
    tk.Button(root_frame, text="Abrir PDV (Vendas)", width=30,
              command=lambda: vendas_ui.abrir_janela_vendas(usuario_logado)).pack(pady=5)

    # ================= Logout =================
    def logout():
        if messagebox.askyesno("Relatório Diário", "Deseja gerar o relatório das vendas de hoje?"):
            arquivo = gerar_relatorio_diario()
            if arquivo:
                messagebox.showinfo("Relatório Gerado", f"Relatório salvo como {arquivo}")
            else:
                messagebox.showinfo("Relatório", "Não houve vendas hoje.")
        root_frame.destroy()
        login_ui.abrir_login(root, abrir_sistema)

    tk.Button(root_frame, text="Logout", width=20, command=logout).pack(pady=10)

    # Fechar aplicação corretamente
    def fechar_app():
        if messagebox.askyesno("Relatório Diário", "Deseja gerar o relatório das vendas de hoje?"):
            arquivo = gerar_relatorio_diario()
            if arquivo:
                messagebox.showinfo("Relatório Gerado", f"Relatório salvo como {arquivo}")
            else:
                messagebox.showinfo("Relatório", "Não houve vendas hoje.")
        db.fechar_conexao()
        root.destroy()

    root_frame.protocol("WM_DELETE_WINDOW", fechar_app)


# ================= Janela de login =================
root = tk.Tk()
root.withdraw()  # esconde janela principal até login


def sair_app():
    db.fechar_conexao()
    root.destroy()


root.protocol("WM_DELETE_WINDOW", sair_app)
login_ui.abrir_login(root, abrir_sistema)
root.mainloop()
