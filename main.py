# main.py
import tkinter as tk
import produtos_ui
import vendas_ui
import usuarios_ui
import db
import login_ui
import empresa_ui

# ================= Inicialização do banco =================
db.criar_tabelas()
db.criar_tabela_usuarios()
db.criar_tabela_empresa()

# Usuários de teste
db.adicionar_usuario("proprietario", "12345", "proprietario")
db.adicionar_usuario("admin", "1234", "admin")
db.adicionar_usuario("funcionario", "1234", "funcionario")

# ================= Função para abrir o sistema =================
def abrir_sistema(tipo_usuario):
    root_frame = tk.Toplevel()
    root_frame.title("PDV Inteligente")

    # Layout de acordo com o tipo de usuário
    if tipo_usuario == "proprietario":
        tk.Button(root_frame, text="Gerenciar Usuários", width=30,
                  command=usuarios_ui.abrir_janela_usuarios).pack(pady=10)
        tk.Button(root_frame, text="Gerenciar Produtos", width=30,
                  command=produtos_ui.abrir_janela_produtos).pack(pady=10)
        tk.Button(root_frame, text="Abrir PDV (Vendas)", width=30,
                  command=lambda: vendas_ui.abrir_janela_vendas(usuario_logado)).pack(pady=10)
        tk.Button(root_frame, text="Configurar Empresa", width=30, 
              command=empresa_ui.abrir_janela_empresa).pack(pady=10)

    elif tipo_usuario == "admin":
        tk.Button(root_frame, text="Gerenciar Produtos", width=30,
                  command=produtos_ui.abrir_janela_produtos).pack(pady=10)
        tk.Button(root_frame, text="Abrir PDV (Vendas)", width=30,
                  command=lambda: vendas_ui.abrir_janela_vendas(usuario_logado)).pack(pady=10)

    else:  # funcionário
        tk.Button(root_frame, text="Abrir PDV (Vendas)", width=30,
                  command=lambda: vendas_ui.abrir_janela_vendas(usuario_logado)).pack(pady=10)

    # Função de logout para voltar ao login
    def logout():
        root_frame.destroy()
        login_ui.abrir_login(root, abrir_sistema)

    tk.Button(root_frame, text="Logout", width=20, command=logout).pack(pady=10)

    # Fechar tudo corretamente
    def fechar_janela():
        db.fechar_conexao()
        root_frame.destroy()
        root.destroy()

    root_frame.protocol("WM_DELETE_WINDOW", fechar_janela)

# ================= Janela de login =================
root = tk.Tk()
root.withdraw()  # esconde janela principal até login

# Guardar usuário logado para registrar vendas
usuario_logado = None

def definir_usuario(tipo):
    global usuario_logado
    usuario_logado = tipo
    abrir_sistema(tipo)

# Ao fechar o login sem entrar
def sair_app():
    db.fechar_conexao()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", sair_app)

# Abrir login inicialmente
login_ui.abrir_login(root, definir_usuario)
root.mainloop()
