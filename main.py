# main.py
import tkinter as tk
import produtos_ui
import vendas_ui
import db
import login_ui
import usuarios_ui
# ================= Inicialização do banco =================
db.criar_tabelas()
db.criar_tabela_usuarios()  # garante que a tabela de usuários exista

# Usuários de teste
db.adicionar_usuario("adm", "1234", "admin")
db.adicionar_usuario("admin", "12345", "proprietario")
db.adicionar_usuario("funcionario", "1234", "funcionario")


# ================= Função para abrir o sistema =================
def abrir_sistema(tipo_usuario):
    root_frame = tk.Toplevel()
    root_frame.title("PDV Inteligente")

    def logout():
        root_frame.destroy()
        login_ui.abrir_login(root, abrir_sistema)


    
    if tipo_usuario == "proprietario":
        tk.Button(root_frame, text="Gerenciar Usuários", width=30, command=usuarios_ui.abrir_janela_usuarios).pack(pady=10)
        tk.Button(root_frame, text="Gerenciar Produtos", width=30, command=produtos_ui.abrir_janela_produtos).pack(pady=10)


    
    tk.Button(root_frame, text="Sair / Logout", width=30, command=logout).pack(pady=10)

    # Fechar tudo corretamente quando fechar a janela do sistema
    def fechar_janela():
        db.fechar_conexao()
        root_frame.destroy()
        root.destroy()  # garante que o loop principal encerre

    root_frame.protocol("WM_DELETE_WINDOW", fechar_janela)

    if tipo_usuario == "admin":
        tk.Button(root_frame, text="Gerenciar Produtos", width=30, 
                  command=produtos_ui.abrir_janela_produtos).pack(pady=10)

    tk.Button(root_frame, text="Abrir PDV (Vendas)", width=30, 
              command=vendas_ui.abrir_janela_vendas).pack(pady=10)

# ================= Janela de login =================
root = tk.Tk()
root.withdraw()  


def sair_app():
    db.fechar_conexao()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", sair_app)

login_ui.abrir_login(root, abrir_sistema)
root.mainloop()
