# usuarios_ui.py
import tkinter as tk
from tkinter import messagebox, simpledialog
import db

def abrir_janela_usuarios():
    janela_usuarios = tk.Toplevel()
    janela_usuarios.title("Gerenciamento de Usuários")
    
    # Lista de usuários
    list_usuarios = tk.Listbox(janela_usuarios, width=50)
    list_usuarios.pack(pady=5)

    def atualizar_lista_usuarios():
        list_usuarios.delete(0, tk.END)
        db.cursor.execute("SELECT id, username, tipo FROM usuarios")
        for user_id, username, tipo in db.cursor.fetchall():
            list_usuarios.insert(tk.END, f"{user_id}: {username} - {tipo}")

    atualizar_lista_usuarios()

    # Adicionar usuário
    def adicionar_usuario():
        username = simpledialog.askstring("Novo Usuário", "Nome de usuário:")
        if not username:
            return
        senha = simpledialog.askstring("Nova Senha", "Senha:", show="*")
        if not senha:
            return
        tipo = simpledialog.askstring("Tipo de Usuário", "Digite 'admin' ou 'funcionario':")
        if tipo not in ("admin", "funcionario"):
            messagebox.showerror("Erro", "Tipo inválido! Use 'admin' ou 'funcionario'.")
            return

        if db.adicionar_usuario(username, senha, tipo):
            messagebox.showinfo("Sucesso", f"Usuário '{username}' adicionado!")
            atualizar_lista_usuarios()
        else:
            messagebox.showerror("Erro", "Usuário já existe!")

    # Alterar usuário
    def alterar_usuario():
        selecao = list_usuarios.curselection()
        if not selecao:
            messagebox.showerror("Erro", "Selecione um usuário para alterar!")
            return
        item = list_usuarios.get(selecao[0])
        user_id, username, tipo_atual = item.split(":")[0], item.split(":")[1].split(" - ")[0], item.split(" - ")[1]

        nova_senha = simpledialog.askstring("Alterar Senha", f"Nova senha para '{username}' (deixe em branco para não alterar):", show="*")
        novo_tipo = simpledialog.askstring("Alterar Tipo", f"Tipo atual: {tipo_atual}\nDigite 'admin' ou 'funcionario':", initialvalue=tipo_atual)
        if novo_tipo not in ("admin", "funcionario"):
            messagebox.showerror("Erro", "Tipo inválido!")
            return

        if nova_senha:
            db.cursor.execute("UPDATE usuarios SET senha=? WHERE id=?", (nova_senha, user_id))
        db.cursor.execute("UPDATE usuarios SET tipo=? WHERE id=?", (novo_tipo, user_id))
        db.conn.commit()
        messagebox.showinfo("Sucesso", f"Usuário '{username}' atualizado!")
        atualizar_lista_usuarios()

    # Remover usuário
    def remover_usuario():
        selecao = list_usuarios.curselection()
        if not selecao:
            messagebox.showerror("Erro", "Selecione um usuário para remover!")
            return
        item = list_usuarios.get(selecao[0])
        user_id, username, tipo = item.split(":")[0], item.split(":")[1].split(" - ")[0], item.split(" - ")[1]

        if tipo == "admin":
            db.cursor.execute("SELECT COUNT(*) FROM usuarios WHERE tipo='admin'")
            qtd_admins = db.cursor.fetchone()[0]
            if qtd_admins <= 1:
                messagebox.showerror("Erro", "Não é possível remover o último administrador!")
                return

        confirmar = messagebox.askyesno("Confirmar", f"Remover usuário '{username}'?")
        if confirmar:
            db.cursor.execute("DELETE FROM usuarios WHERE id=?", (user_id,))
            db.conn.commit()
            messagebox.showinfo("Sucesso", f"Usuário '{username}' removido!")
            atualizar_lista_usuarios()

    tk.Button(janela_usuarios, text="Adicionar Usuário", command=adicionar_usuario).pack(pady=5)
    tk.Button(janela_usuarios, text="Alterar Usuário", command=alterar_usuario).pack(pady=5)
    tk.Button(janela_usuarios, text="Remover Usuário", command=remover_usuario).pack(pady=5)
