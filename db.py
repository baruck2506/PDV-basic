# db.py
import sqlite3
from datetime import datetime

# ================= Conexão =================
conn = sqlite3.connect("pdv.db")
cursor = conn.cursor()

# ================= Criação de Tabelas =================
def criar_tabelas():
    # Produtos
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS produtos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT UNIQUE,
        preco REAL,
        estoque INTEGER
    )
    """)
    # Vendas
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS vendas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        total REAL,
        data TEXT,
        funcionario TEXT
    )
    """)
    # Itens de Venda
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

# Usuários
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
        cursor.execute(
            "INSERT INTO usuarios (username, senha, tipo) VALUES (?, ?, ?)",
            (username, senha, tipo)
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False

def autenticar_usuario(username, senha):
    cursor.execute(
        "SELECT tipo FROM usuarios WHERE username=? AND senha=?",
        (username, senha)
    )
    resultado = cursor.fetchone()
    if resultado:
        return resultado[0]  # 'admin', 'funcionario', 'proprietario'
    return None

def listar_usuarios():
    cursor.execute("SELECT id, username, tipo FROM usuarios")
    return cursor.fetchall()

def remover_usuario(username):
    cursor.execute("DELETE FROM usuarios WHERE username=?", (username,))
    conn.commit()

def alterar_usuario(username, novo_username, nova_senha, novo_tipo):
    cursor.execute("""
        UPDATE usuarios
        SET username=?, senha=?, tipo=?
        WHERE username=?
    """, (novo_username, nova_senha, novo_tipo, username))
    conn.commit()

# Produtos
def adicionar_produto(nome, preco, estoque):
    try:
        cursor.execute(
            "INSERT INTO produtos (nome, preco, estoque) VALUES (?, ?, ?)",
            (nome, preco, estoque)
        )
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
    return cursor.fetchall()  # lista de tuplas (id, nome, preco, estoque)

# Estoque
def atualizar_estoque(nome, nova_quantidade):
    cursor.execute("UPDATE produtos SET estoque=? WHERE nome=?", (nova_quantidade, nome))
    conn.commit()

# Vendas
def salvar_venda(carrinho, funcionario):
    total_venda = 0
    for nome, qtd in carrinho.items():
        cursor.execute("SELECT id, preco FROM produtos WHERE nome=?", (nome,))
        produto_id, preco = cursor.fetchone()
        total_venda += preco * qtd

    data_atual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute(
        "INSERT INTO vendas (total, data, funcionario) VALUES (?, ?, ?)",
        (total_venda, data_atual, funcionario)
    )
    venda_id = cursor.lastrowid

    for nome, qtd in carrinho.items():
        cursor.execute("SELECT id FROM produtos WHERE nome=?", (nome,))
        produto_id = cursor.fetchone()[0]
        cursor.execute(
            "INSERT INTO itens_venda (venda_id, produto_id, quantidade) VALUES (?, ?, ?)",
            (venda_id, produto_id, qtd)
        )
    conn.commit()

def listar_vendas():
    cursor.execute("SELECT id, total, data, funcionario FROM vendas")
    return cursor.fetchall()

def listar_itens_venda(venda_id):
    cursor.execute("""
        SELECT p.nome, iv.quantidade, p.preco
        FROM itens_venda iv
        JOIN produtos p ON iv.produto_id = p.id
        WHERE iv.venda_id=?
    """, (venda_id,))
    return cursor.fetchall()  # lista de tuplas (nome, quantidade, preco)

# Empresa
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

def salvar_empresa(nome, cnpj, endereco, telefone):
    cursor.execute("DELETE FROM empresa")  # apenas um registro
    cursor.execute(
        "INSERT INTO empresa (nome, cnpj, endereco, telefone) VALUES (?, ?, ?, ?)",
        (nome, cnpj, endereco, telefone)
    )
    conn.commit()

def carregar_empresa():
    cursor.execute("SELECT nome, cnpj, endereco, telefone FROM empresa LIMIT 1")
    return cursor.fetchone()  # tupla ou None

def obter_preco_produto(nome):
    cursor.execute("SELECT preco FROM produtos WHERE nome=?", (nome,))
    resultado = cursor.fetchone()
    if resultado:
        return resultado[0]
    return 0


# Encerrar conexão
def fechar_conexao():
    conn.close()
