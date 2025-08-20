# db.py
import sqlite3
from datetime import datetime

# Conexão com o banco
conn = sqlite3.connect("pdv.db")
cursor = conn.cursor()

# ================= Criação das tabelas =================
def criar_tabelas():
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS produtos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT UNIQUE,
        preco REAL,
        estoque INTEGER
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS vendas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        total REAL,
        data TEXT
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS itens_venda (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        venda_id INTEGER,
        produto_id INTEGER,
        quantidade INTEGER,
        FOREIGN KEY(venda_id) REFERENCES vendas(id),
        FOREIGN KEY(produto_id) REFERENCES produtos(id)
    )
    """)
    conn.commit()

# db.py (adição)
def criar_tabela_usuarios():
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        senha TEXT,
        tipo TEXT
    )
    """)
    conn.commit()

def adicionar_usuario(username, senha, tipo):
    try:
        cursor.execute("INSERT INTO usuarios (username, senha, tipo) VALUES (?, ?, ?)", (username, senha, tipo))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False

def autenticar_usuario(username, senha):
    cursor.execute("SELECT tipo FROM usuarios WHERE username=? AND senha=?", (username, senha))
    resultado = cursor.fetchone()
    if resultado:
        return resultado[0]  # retorna 'admin' ou 'funcionario'
    return None


# ================= Funções de Produtos =================
def adicionar_produto(nome, preco, estoque):
    try:
        cursor.execute("INSERT INTO produtos (nome, preco, estoque) VALUES (?, ?, ?)", (nome, preco, estoque))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False

def remover_produto(nome):
    cursor.execute("DELETE FROM produtos WHERE nome=?", (nome,))
    conn.commit()

def alterar_produto(nome_atual, novo_nome, novo_preco, novo_estoque):
    cursor.execute("""
        UPDATE produtos
        SET nome=?, preco=?, estoque=?
        WHERE nome=?
    """, (novo_nome, novo_preco, novo_estoque, nome_atual))
    conn.commit()

def listar_produtos():
    cursor.execute("SELECT id, nome, preco, estoque FROM produtos")
    return cursor.fetchall()  # Lista de tuplas (id, nome, preco, estoque)

# ================= Funções de Vendas =================
def salvar_venda(carrinho):
    total_venda = 0
    for nome, qtd in carrinho.items():
        cursor.execute("SELECT id, preco FROM produtos WHERE nome=?", (nome,))
        produto_id, preco = cursor.fetchone()
        total_venda += preco * qtd

    data_atual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("INSERT INTO vendas (total, data) VALUES (?, ?)", (total_venda, data_atual))
    venda_id = cursor.lastrowid

    for nome, qtd in carrinho.items():
        cursor.execute("SELECT id FROM produtos WHERE nome=?", (nome,))
        produto_id = cursor.fetchone()[0]
        cursor.execute("INSERT INTO itens_venda (venda_id, produto_id, quantidade) VALUES (?, ?, ?)",
                       (venda_id, produto_id, qtd))
    conn.commit()

# ================= Funções de Estoque =================
def atualizar_estoque(nome, nova_quantidade):
    cursor.execute("UPDATE produtos SET estoque=? WHERE nome=?", (nova_quantidade, nome))
    conn.commit()

def fechar_conexao():
    conn.close()

    