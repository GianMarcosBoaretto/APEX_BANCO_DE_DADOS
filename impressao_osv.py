from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import Image
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from datetime import datetime
from conexao import conectar
import os

conexao = conectar()

def obter_dados_osv(osv_id, ano):
    if conexao:
        try:
            cursor = conexao.cursor()

            consulta_osv = """
                SELECT ordem_servico.id, ordem_servico.ano, 
                    ordem_servico.data_cadastro, ordem_servico.modelo, 
                    ordem_servico.descricao, ordem_servico.observacao 
                FROM ordem_servico 
                WHERE ordem_servico.id = %s AND ordem_servico.ano = %s
            """
            cursor.execute(consulta_osv, (osv_id, ano))
            dados_osv = cursor.fetchone()

            if dados_osv: 
                consulta_produtos = """
                    SELECT ordem_servico_produtos.produto_id, produtos.nome, ordem_servico_produtos.sequencial, 
                        ordem_servico_produtos.quantidade, ordem_servico_produtos.valor_unitario, 
                        ordem_servico_produtos.valor_total 
                    FROM ordem_servico_produtos 
                    JOIN produtos ON produtos.id = ordem_servico_produtos.produto_id
                    WHERE ordem_servico_produtos.osv_id = %s AND ordem_servico_produtos.ano = %s
                    """
                cursor.execute(consulta_produtos, (osv_id, ano))
                produtos = cursor.fetchall()

                consulta_servicos = """
                    SELECT ordem_servico_servicos.servico_id, produtos.nome, ordem_servico_servicos.sequencial, 
                        ordem_servico_servicos.quantidade, ordem_servico_servicos.valor_unitario, 
                        ordem_servico_servicos.valor_total 
                    FROM ordem_servico_servicos 
                    JOIN produtos ON produtos.id = ordem_servico_servicos.servico_id
                    WHERE ordem_servico_servicos.osv_id = %s AND ordem_servico_servicos.ano = %s
                    """
                cursor.execute(consulta_servicos, (osv_id, ano))
                servicos = cursor.fetchall()

                consulta_clientes = """
                    SELECT clientes.nome, clientes.cpf, cidades.nome AS cidade, clientes.telefone
                    FROM clientes
                    JOIN cidades ON clientes.cidade_id = CIDADES.ID
                    JOIN ordem_servico ON ordem_servico.cliente_id = clientes.id
                    WHERE ordem_servico.id = %s AND ordem_servico.ano = %s
                    """
                cursor.execute(consulta_clientes, (osv_id, ano))
                clientes = cursor.fetchall()

                print("Clientes encontrados:", clientes)  # Verifique os dados retornados

                gerar_pdf_osv(dados_osv, produtos, servicos, clientes)
                return dados_osv, produtos, servicos, clientes, 
            else:
                print(f"Ordem de serviço com ID {osv_id} não encontrada.")
                return None, None, None

        except Exception as e:
            print(f"Erro ao consultar o banco de dados: {e}")
            return None, None, None
        

def gerar_pdf_osv(dados_osv, produtos, servicos, clientes, caminho_arquivo="ordem_servico.pdf"):


    script_dir = os.path.dirname(os.path.abspath(__file__))  # Diretório onde o script está
    logo_path = os.path.join(script_dir, "logo.png")  # Caminho relativo para a logo

    # Inicializando o documento
    doc = SimpleDocTemplate(caminho_arquivo, pagesize=A4)
    
    # Inicializando os elementos para adicionar no PDF
    elementos = []

    # Criando os estilos
    styles = getSampleStyleSheet()
    estilo_titulo = ParagraphStyle(name='Titulo', fontSize=24, alignment=1)  # Maior tamanho para título (24)
    estilo_normal = ParagraphStyle(name='Normal', fontSize=16)  # Maior tamanho para texto normal (16)

    if clientes:
        nome_cliente, cpf, cidade, telefone = clientes[0]  # Desempacotando a tupla
    else:
        print("Nenhum cliente encontrado.")
        return  # ou trate o erro de outra forma


    # Dados da OS
    numero = dados_osv[0]
    ano = dados_osv[1]
    data = dados_osv[2].strftime("%d/%m/%Y") if hasattr(dados_osv[2], "strftime") else str(dados_osv[2])
    modelo = dados_osv[3]
    descricao = dados_osv[4]
    observacao = dados_osv[5]

    try:
        imagem_logo = Image(logo_path, width=400, height=100)  # Ajuste o tamanho conforme necessário
        elementos.append(imagem_logo)
    except Exception as e:
        print(f"Erro ao carregar a logo: {e}")
    
    elementos.append(Spacer(1, 12))


    # Adicionando o título
    elementos.append(Paragraph("Ordem de Serviço {numero}", styles['Title']))
    elementos.append(Spacer(1, 12))

    # Dados do cliente
    elementos.append(Paragraph(f"Cliente: {nome_cliente}", estilo_normal))
    elementos.append(Paragraph(f"CPF: {cpf}", estilo_normal))
    elementos.append(Paragraph(f"Cidade: {cidade}", estilo_normal))
    elementos.append(Paragraph(f"Telefone: {telefone}", estilo_normal))
    elementos.append(Spacer(1, 12))

    # Dados da OS
    elementos.append(Paragraph(f"Número: {numero}/{ano}", estilo_normal))
    elementos.append(Spacer(1, 12))
    elementos.append(Paragraph(f"Data: {data}", estilo_normal))
    elementos.append(Spacer(1, 12))
    elementos.append(Paragraph(f"Modelo: {modelo}", estilo_normal))
    elementos.append(Spacer(1, 12))
    elementos.append(Paragraph(f"Descrição: {descricao}", estilo_normal))
    elementos.append(Spacer(1, 12))
    elementos.append(Paragraph(f"Observação: {observacao}", estilo_normal))
    elementos.append(Spacer(1, 12))

    # Produtos
    elementos.append(Paragraph("Produtos:", estilo_normal))
    for produto in produtos:
        nome_produto = produto[1]
        quantidade = produto[3]
        valor_unitario = produto[4]
        valor_total = produto[5]
        elementos.append(Paragraph(f"Produto: {nome_produto} | Quantidade: {quantidade} | Unit: R$ {valor_unitario:.2f} | Total: R$ {valor_total:.2f}", estilo_normal))
        elementos.append(Spacer(1, 12))
    
    elementos.append(Spacer(1, 24))

    # Serviços
    elementos.append(Paragraph("Serviços:", estilo_normal))
    for servico in servicos:
        nome_servico = servico[1]
        quantidade = servico[3]
        valor_unitario = servico[4]
        valor_total = servico[5]
        elementos.append(Paragraph(f"Serviço: {nome_servico} | Quantidade: {quantidade} | Unit: R$ {valor_unitario:.2f} | Total: R$ {valor_total:.2f}", estilo_normal))
        elementos.append(Spacer(1, 24))

    # Rodapé com assinaturas e informações da empresa
    elementos.append(Spacer(1, 12))
    elementos.append(Paragraph(f"Data: {data}", estilo_normal))
    elementos.append(Spacer(1, 12))
    elementos.append(Paragraph("Assinatura do Cliente: ______________________", estilo_normal))
    elementos.append(Spacer(1, 18))
    elementos.append(Paragraph("AV. XV DE NOVEMBRO, 535, SALA 117, CENTRO, JOAÇABA", estilo_normal))
    elementos.append(Spacer(1, 18))
    elementos.append(Paragraph("FONE: (49) 3521-1454 OU (49) 9 9111-2696", estilo_normal))

    # Gerando o PDF
    doc.build(elementos)
    print(f"PDF gerado com sucesso: {caminho_arquivo}")
