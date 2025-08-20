# cupom.py
import db
from datetime import datetime

def gerar_cupom(carrinho, funcionario):
    # Carregar dados da empresa
    empresa = db.carregar_empresa()
    if empresa:
        nome_empresa, cnpj, endereco, telefone = empresa
    else:
        nome_empresa, cnpj, endereco, telefone = ("N/D", "N/D", "N/D", "N/D")

    # Nome do arquivo com timestamp
    agora = datetime.now()
    nome_arquivo = f"Cupom_{agora.strftime('%Y%m%d_%H%M%S')}.txt"

    total = 0

    with open(nome_arquivo, "w", encoding="utf-8") as f:
        # Cabeçalho da empresa
        f.write(f"{nome_empresa}\n")
        f.write(f"CNPJ: {cnpj}\n")
        f.write(f"Endereço: {endereco}\n")
        f.write(f"Telefone: {telefone}\n")
        f.write("-" * 40 + "\n")
        f.write(f"Data: {agora.strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Funcionário: {funcionario}\n")
        f.write("-" * 40 + "\n")
        f.write(f"{'Produto':20} {'Qtd':>3} {'Preço':>7} {'Subtotal':>10}\n")
        f.write("-" * 40 + "\n")

        for nome, qtd in carrinho.items():
            preco = db.obter_preco_produto(nome)
            subtotal = preco * qtd
            total += subtotal
            f.write(f"{nome:20} {qtd:>3} {preco:>7.2f} {subtotal:>10.2f}\n")

        f.write("-" * 40 + "\n")
        f.write(f"{'TOTAL:':>32} R$ {total:.2f}\n")
        f.write("-" * 40 + "\n")

    return nome_arquivo
