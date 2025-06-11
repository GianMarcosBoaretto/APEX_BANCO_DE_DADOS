# os_dados.py
from conexao import conectar

def carregar_ordem_servico(osv_id, ano):
    conexao = conectar()
    if not conexao:
        return None
    cursor = conexao.cursor()
    cursor.execute("""
    SELECT ordem_servico.id, ordem_servico.ano, ordem_servico.cliente_id, clientes.nome, ordem_servico.data_cadastro, ordem_servico.modelo,
           ordem_servico.descricao, ordem_servico.observacao, ordem_servico.valor_total
    FROM ordem_servico
    INNER JOIN clientes ON ordem_servico.cliente_id = clientes.id
    WHERE ordem_servico.id = %s
    and ordem_servico.ano = %s
    """, (osv_id, ano))

    dados = cursor.fetchone()
    cursor.close()
    conexao.close()
    return dados

def salvar_ordem_servico(osv_id, cliente_id, data, modelo, descricao, observacao, ano):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        UPDATE ordem_servico
        SET cliente_id=%s, data_cadastro=%s, modelo=%s, descricao=%s, observacao=%s
        WHERE id=%s
        and ano = %s
    """, (cliente_id, data, modelo, descricao, observacao, osv_id, ano))
    conexao.commit()
    cursor.close()
    conexao.close()

    
def recarregar(osv_id, ano):
    conexao = conectar()
    if not conexao:
        return None
    cursor = conexao.cursor()
    cursor.execute("""
    SELECT ordem_servico.id, ordem_servico.ano, ordem_servico.cliente_id, clientes.nome, ordem_servico.data_cadastro, ordem_servico.modelo,
           ordem_servico.descricao, ordem_servico.observacao, ordem_servico.valor_total
    FROM ordem_servico
    INNER JOIN clientes ON ordem_servico.cliente_id = clientes.id
    WHERE ordem_servico.id = %s
    and ordem_servico.ano = %s
    """, (osv_id, ano))

    dados = cursor.fetchone()
    cursor.close()
    conexao.close()
    return dados
