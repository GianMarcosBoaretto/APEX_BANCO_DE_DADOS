
from conexao import conectar

def carregar_servicos_da_ordem(osv_id):
    conexao = conectar()
    if not conexao:
        return []
    cursor = conexao.cursor()
    cursor.execute("""
        SELECT servico_id, quantidade, valor
        FROM ordem_servico_servicos
        WHERE osv_id = %s
    """, (osv_id,))
    produtos = cursor.fetchall()
    cursor.close()
    conexao.close()
    return produtos

def adicionar_servicos_na_ordem(osv_id, produto_id, quantidade, sequencial, valor_unitario, valor_total, ano):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        INSERT INTO ordem_servico_servicos (osv_id, servico_id, quantidade, sequencial, valor_unitario, valor_total, ano)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (osv_id, produto_id, quantidade, sequencial, valor_unitario ,valor_total, ano))
    conexao.commit()
    cursor.close()
    conexao.close()
