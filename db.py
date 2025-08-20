# db.py
import sqlite3
from datetime import datetime

# ================= Conexão com o banco =================
conn = sqlite3.connect("pdv.db")
cursor = conn.cursor()

# ================= Criação de tabelas =================
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
            data TEXT,
            funcionario TEXT
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

def criar_tabela_empresa():
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS empresa (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            cnpj TEXT,
            endereco TEXT,
            telefone TEXT
        )
    """)
    conn.commit()

# ================= Usuários =================
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
        return resultado[0]
    return None

def listar_usuarios():
    cursor.execute("SELECT id, username, tipo FROM usuarios")
    return cursor.fetchall()

def remover_usuario(username):
    cursor.execute("DELETE FROM usuarios WHERE username=?", (username,))
    conn.commit()

def alterar_usuario(username_atual, novo_username, novo_tipo):
    cursor.execute("""
        UPDATE usuarios
        SET username=?, tipo=?
        WHERE username=?
    """, (novo_username, novo_tipo, username_atual))
    conn.commit()

# ================= Produtos =================
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
    return cursor.fetchall()

# ================= Vendas =================
def salvar_venda(carrinho, funcionario):
    total_venda = 0
    for nome, qtd in carrinho.items():
        cursor.execute("SELECT id, preco FROM produtos WHERE nome=?", (nome,))
        produto_id, preco = cursor.fetchone()
        total_venda += preco * qtd

    data_atual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("INSERT INTO vendas (total, data, funcionario) VALUES (?, ?, ?)", (total_venda, data_atual, funcionario))
    venda_id = cursor.lastrowid

    for nome, qtd in carrinho.items():
        cursor.execute("SELECT id FROM produtos WHERE nome=?", (nome,))
        produto_id = cursor.fetchone()[0]
        cursor.execute("INSERT INTO itens_venda (venda_id, produto_id, quantidade) VALUES (?, ?, ?)",
                       (venda_id, produto_id, qtd))
    conn.commit()

def listar_vendas_por_data(data):
    cursor.execute("SELECT id, total, data, funcionario FROM vendas WHERE date(data)=?", (data,))
    vendas = cursor.fetchall()
    relatorio = []
    for venda_id, total, data_venda, funcionario in vendas:
        cursor.execute("""
            SELECT produtos.nome, produtos.preco, itens_venda.quantidade
            FROM itens_venda
            JOIN produtos ON itens_venda.produto_id = produtos.id
            WHERE itens_venda.venda_id=?
        """, (venda_id,))
        itens = cursor.fetchall()
        relatorio.append({
            "data": data_venda,
            "funcionario": funcionario,
            "total": total,
            "itens": [{"nome": n, "preco": p, "quantidade": q, "subtotal": p*q} for n, p, q in itens]
        })
    return relatorio

# ================= Estoque =================
def atualizar_estoque(nome, nova_quantidade):
    cursor.execute("UPDATE produtos SET estoque=? WHERE nome=?", (nova_quantidade, nome))
    conn.commit()

# ================= Empresa =================
def salvar_empresa(nome, cnpj, endereco, telefone):
    cursor.execute("DELETE FROM empresa")  # Mantém apenas um registro
    cursor.execute("INSERT INTO empresa (nome, cnpj, endereco, telefone) VALUES (?, ?, ?, ?)",
                   (nome, cnpj, endereco, telefone))
    conn.commit()

def carregar_empresa():
    cursor.execute("SELECT nome, cnpj, endereco, telefone FROM empresa LIMIT 1")
    return cursor.fetchone()

# ================= Conexão =================
def fechar_conexao():
    conn.close()
