# os_edicao.py
import tkinter as tk
from tkinter import ttk, messagebox
from os_dados import carregar_ordem_servico, salvar_ordem_servico
from os_produtos import adicionar_produto_na_ordem
from os_servicos import adicionar_servicos_na_ordem
from conexao import conectar
from decimal import Decimal
import datetime  # Para pegar o ano atual
import os_editar
from impressao_padrao_osv import obter_dados_osv

def abrir_edicao_ordem_servico(osv_id, ano):
    dados = carregar_ordem_servico(osv_id, ano)
    if not dados:
        messagebox.showerror("Erro", "Ordem de serviço não encontrada.")
        return
    id, ano, cliente_id, nome_cliente, data, modelo, descricao, observacao, valor_total = dados

    data_convert = data_formatada = data.strftime("%d-%m-%Y")

    janela = tk.Tk()
    janela.title(f"Editar Ordem de Serviço {osv_id}/{ano}")
    janela.geometry("700x500")

    def aba_mudada(event):
        aba_atual = notebook.index("current")
        print("Mudou e achou")
        if aba_atual == 0:
            dados = carregar_ordem_servico(osv_id, ano)
            id, ano_2, cliente_id, nome_cliente, data, modelo, descricao, observacao, valor_total = dados
            tk.Label(frame_os, text="Valor Total").grid(row=0, column=2, padx=5)
            entry_valor_total = tk.Entry(frame_os, state="normal", width=10)
            entry_valor_total.insert(0, valor_total)
            entry_valor_total.configure(state="readonly")
            entry_valor_total.grid(row=1, column=2, padx=5)

    notebook = ttk.Notebook(janela)
    aba_dados = ttk.Frame(notebook)
    aba_produtos = ttk.Frame(notebook)
    aba_servicos = ttk.Frame(notebook)

    notebook.add(aba_dados, text="Dados da OS")
    notebook.add(aba_produtos, text="Produtos")
    notebook.add(aba_servicos, text="Serviços")
    notebook.pack(expand=1, fill="both")
    notebook.bind("<<NotebookTabChanged>>", aba_mudada)

    # Dados - ID e Ano
    frame_os = tk.Frame(aba_dados)
    frame_os.pack(pady=5)

    tk.Label(frame_os, text="Número da OS (ID)").grid(row=0, column=0, padx=5)
    entry_id = tk.Entry(frame_os, state="normal", width=15)
    entry_id.insert(0, id)
    entry_id.configure(state="readonly")
    entry_id.grid(row=1, column=0, padx=5)

    tk.Label(frame_os, text="Ano").grid(row=0, column=1, padx=5)
    entry_ano = tk.Entry(frame_os, state="normal", width=10)
    entry_ano.insert(0, ano)
    entry_ano.configure(state="readonly")
    entry_ano.grid(row=1, column=1, padx=5)

    tk.Label(frame_os, text="Valor Total").grid(row=0, column=2, padx=5)
    entry_valor_total = tk.Entry(frame_os, state="normal", width=10)
    entry_valor_total.insert(0, valor_total)
    entry_valor_total.configure(state="readonly")
    entry_valor_total.grid(row=1, column=2, padx=5)

    # Nome do Cliente e Data
    frame_cliente_data = tk.Frame(aba_dados)
    frame_cliente_data.pack(pady=5)

    tk.Label(frame_cliente_data, text="Nome do Cliente:").grid(row=0, column=0, padx=5)
    entry_cliente = tk.Entry(frame_cliente_data, state="normal", width=30)
    entry_cliente.insert(0, nome_cliente)
    entry_cliente.configure(state="readonly")
    entry_cliente.grid(row=1, column=0, padx=5)

    tk.Label(frame_cliente_data, text="Data (DD-MM-AAAA):").grid(row=0, column=1, padx=5)
    entry_data = tk.Entry(frame_cliente_data, width=15)
    entry_data.insert(0, data_convert)
    entry_data.grid(row=1, column=1, padx=5)

    # Modelo
    tk.Label(aba_dados, text="Modelo:").pack()
    entry_modelo = tk.Entry(aba_dados)
    entry_modelo.insert(0, modelo)
    entry_modelo.pack()

    # Descrição
    tk.Label(aba_dados, text="Descrição:").pack()
    text_descricao = tk.Text(aba_dados, height=3)
    text_descricao.insert("1.0", descricao)
    text_descricao.pack()

    # Observação
    tk.Label(aba_dados, text="Observação:").pack()
    text_observacao = tk.Text(aba_dados, height=3)
    text_observacao.insert("1.0", observacao)
    text_observacao.pack()

    def imprimir():
        obter_dados_osv(osv_id, ano)

    def consulta():
        janela.destroy()
        os_editar.abrir_seletor_ordens()    

    def salvar_edicao():
        nova_data = entry_data.get().strip()
        novo_modelo = entry_modelo.get()
        nova_desc = text_descricao.get("1.0", tk.END).strip()
        nova_obs = text_observacao.get("1.0", tk.END).strip()

        try:
            nova_data_convertida = datetime.datetime.strptime(nova_data, "%d-%m-%Y").strftime("%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Erro", "Data inválida. Use o formato DD-MM-AAAA.")
            return

        salvar_ordem_servico(osv_id, cliente_id, nova_data_convertida, novo_modelo, nova_desc, nova_obs, ano)
        messagebox.showinfo("Salvo", "Dados atualizados com sucesso.")

    tk.Button(aba_dados, text="Salvar Alterações", command=salvar_edicao).pack(pady=10)
    tk.Button(aba_dados, text="Realizar nova Consulta", command=consulta).pack(pady=10)
    tk.Button(aba_dados, text="Impressão de OSV", command=imprimir).pack(pady=10)

    # Produtos
    from_produto_id = tk.StringVar()
    entry_qtd = tk.StringVar()

    frame_lista = tk.Frame(aba_produtos)
    frame_lista.pack(fill="both", expand=True)

    colunas = ('produto_id', 'nome', 'sequencial', 'quantidade', 'valor_unitario', 'valor_total')
    tree_prod = ttk.Treeview(frame_lista, columns=colunas, show='headings')
    for col in colunas:
        tree_prod.heading(col, text=col.title())
    tree_prod.pack(fill="both", expand=True)

    def atualizar_lista_produtos():
        for item in tree_prod.get_children():
            tree_prod.delete(item)

        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute("""
            SELECT osp.produto_id, p.nome, osp.sequencial, osp.quantidade, osp.valor_unitario, osp.valor_total
            FROM ordem_servico_produtos osp
            JOIN produtos p ON osp.produto_id = p.id
            WHERE osp.osv_id = %s
            and osp.ano = %s
            ORDER BY osp.sequencial           
        """, (osv_id, ano))
        for prod in cursor.fetchall():
            tree_prod.insert('', tk.END, values=prod)
        cursor.close()
        conexao.close()

    frame_add = tk.Frame(aba_produtos)
    frame_add.pack(pady=10)

    produtos_disponiveis = []
    produto_ids = {}

    def carregar_produtos_disponiveis():
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute("SELECT id, nome FROM produtos WHERE fl_servico = 0 and fl_inativo = 0 ORDER BY nome")
        produtos = cursor.fetchall()
        cursor.close()
        conexao.close()
        return produtos

    produtos_disponiveis = carregar_produtos_disponiveis()
    produto_ids = {f"{nome} (ID: {id})": id for id, nome in produtos_disponiveis}

    tk.Label(frame_add, text="Produto:").grid(row=0, column=0)
    combo_produto = ttk.Combobox(frame_add, values=list(produto_ids.keys()), state="readonly", width=40)
    combo_produto.grid(row=0, column=1)

    tk.Label(frame_add, text="Quantidade:").grid(row=0, column=2)
    entry_qtd = tk.Entry(frame_add, width=10)
    entry_qtd.grid(row=0, column=3)

    def adicionar_produto():
        nome_prod = combo_produto.get()
        if not nome_prod:
            messagebox.showwarning("Aviso", "Selecione um produto.")
            return
        
        qtd_str = entry_qtd.get()
        if not qtd_str or not qtd_str.isdigit():  # Verifica se a quantidade é um número válido
            messagebox.showerror("Erro", "Por favor, insira uma quantidade válida.")
            return

        try:
            prod_id = produto_ids[nome_prod]
            qtd = Decimal(entry_qtd.get())

            conexao = conectar()
            cursor = conexao.cursor()

            cursor.execute("SELECT valor_venda, quantidade_estoque FROM produtos WHERE id = %s", (prod_id,))
            resultado = cursor.fetchone()
            if not resultado:
                raise Exception("Produto não encontrado.")
            
            valor_unitario = Decimal(resultado[0]) 
            estoque = resultado[1]

            if qtd > estoque:
                messagebox.showerror("Erro", f"Estoque insuficiente. Atual: {estoque}")
                return

            valor_total = valor_unitario * qtd

            cursor.execute("SELECT COALESCE(MAX(sequencial), 0) + 1 FROM ordem_servico_produtos WHERE osv_id = %s", (osv_id,))
            sequencial = cursor.fetchone()[0]

            adicionar_produto_na_ordem(osv_id, prod_id, qtd, sequencial, valor_unitario, valor_total, ano)

            cursor.execute("""
                UPDATE produtos SET quantidade_estoque = quantidade_estoque - %s
                WHERE id = %s
            """, (qtd, prod_id))

            cursor.execute("""
                UPDATE ordem_servico 
                SET valor_total = (
                    COALESCE((
                        SELECT SUM(ordem_servico_produtos.valor_total) 
                        FROM ordem_servico_produtos
                        WHERE ordem_servico_produtos.osv_id = %s AND ordem_servico_produtos.ano = %s
                    ), 0) + 
                    COALESCE((
                        SELECT SUM(ordem_servico_servicos.valor_total) 
                        FROM ordem_servico_servicos
                        WHERE ordem_servico_servicos.osv_id = %s AND ordem_servico_servicos.ano = %s
                    ), 0)
                )
                WHERE ordem_servico.id = %s AND ordem_servico.ano = %s
            """, (osv_id, ano, osv_id, ano, osv_id, ano))
            
            conexao.commit()
            cursor.close()
            conexao.close()

            atualizar_lista_produtos()
            combo_produto.set("")
            entry_qtd.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    tk.Button(frame_add, text="Adicionar Produto", command=adicionar_produto).grid(row=0, column=4, padx=10)

    def excluir_produto():
        item = tree_prod.selection()
        if not item:
            messagebox.showwarning("Aviso", "Selecione um item para excluir.")
            return

        produto_id, nome, sequencial, quantidade, valor_unitario, valor_total = tree_prod.item(item)['values']

        if not messagebox.askyesno("Confirmação", "Deseja excluir este produto da OS?"):
            return

        conexao = conectar()
        cursor = conexao.cursor()

        sequencial = int(sequencial)

        # Devolver ao estoque
        cursor.execute("""
            UPDATE produtos SET quantidade_estoque = quantidade_estoque + %s
            WHERE id = %s
        """, (quantidade, produto_id))

        # Excluir apenas esse item
        cursor.execute("""
            DELETE FROM ordem_servico_produtos
            WHERE osv_id = %s AND sequencial = %s
            and ano = %s
        """, (osv_id, sequencial, ano))

        cursor.execute("""
            UPDATE ordem_servico 
            SET valor_total = (
                COALESCE((
                    SELECT SUM(ordem_servico_produtos.valor_total) 
                    FROM ordem_servico_produtos
                    WHERE ordem_servico_produtos.osv_id = %s AND ordem_servico_produtos.ano = %s
                ), 0) + 
                COALESCE((
                    SELECT SUM(ordem_servico_servicos.valor_total) 
                    FROM ordem_servico_servicos
                    WHERE ordem_servico_servicos.osv_id = %s AND ordem_servico_servicos.ano = %s
                ), 0)
            )
            WHERE ordem_servico.id = %s AND ordem_servico.ano = %s
        """, (osv_id, ano, osv_id, ano, osv_id, ano))

   
        conexao.commit()
        cursor.close()
        conexao.close()

        atualizar_lista_produtos()

    tk.Button(frame_add, text="Excluir Produto", command=excluir_produto).grid(row=1, column=0, columnspan=5, pady=10)

    atualizar_lista_produtos()

    # Serviço
    from_produto_id = tk.StringVar()
    entry_qtd_serv = tk.StringVar()

    frame_lista = tk.Frame(aba_servicos)
    frame_lista.pack(fill="both", expand=True)

    colunas = ('servico_id', 'nome', 'sequencial', 'quantidade', 'valor_unitario', 'valor_total')
    tree = ttk.Treeview(frame_lista, columns=colunas, show='headings')
    for col in colunas:
        tree.heading(col, text=col.title())
    tree.pack(fill="both", expand=True)

    def atualizar_lista_servicos():
        for item in tree.get_children():
            tree.delete(item)

        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute("""
            SELECT oss.servico_id, p.nome, oss.sequencial, oss.quantidade, oss.valor_unitario, oss.valor_total
            FROM ordem_servico_servicos oss
            JOIN produtos p ON oss.servico_id = p.id
            WHERE oss.osv_id = %s
            and oss.ano = %s
            ORDER BY oss.sequencial
        """, (osv_id, ano))
        for serv in cursor.fetchall():
            tree.insert('', tk.END, values=serv)
        cursor.close()
        conexao.close()


    frame_add = tk.Frame(aba_servicos)
    frame_add.pack(pady=10)

    servicos_disponiveis = []
    servicos_ids = {}

    def carregar_servicos_disponiveis():
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute("SELECT id, nome FROM produtos WHERE fl_servico = 1 AND fl_inativo = 0 ORDER BY nome")
        servicos = cursor.fetchall()
        cursor.close()
        conexao.close()
        return servicos

    servicos_disponiveis = carregar_servicos_disponiveis()
    servicos_ids = {f"{nome} (ID: {id})": id for id, nome in servicos_disponiveis}

    tk.Label(frame_add, text="Serviço:").grid(row=0, column=0)
    combo_servico = ttk.Combobox(frame_add, values=list(servicos_ids.keys()), state="readonly", width=40)
    combo_servico.grid(row=0, column=1)

    tk.Label(frame_add, text="Quantidade:").grid(row=0, column=2)
    entry_qtd_serv = tk.Entry(frame_add, width=10)
    entry_qtd_serv.grid(row=0, column=3)

    def adicionar_servico():
        nome_serv = combo_servico.get()
        if not nome_serv:
            messagebox.showwarning("Aviso", "Selecione um serviço.")
            return

        qtd_str_serv = entry_qtd_serv.get()
        if not qtd_str_serv or not qtd_str_serv.isdigit():
            messagebox.showerror("Erro", "Por favor, insira uma quantidade válida.")
            return

        try:
            serv_id = servicos_ids[nome_serv]
            qtd_serv = Decimal(qtd_str_serv)

            conexao = conectar()
            cursor = conexao.cursor()

            cursor.execute("SELECT valor_venda FROM produtos WHERE id = %s", (serv_id,))
            resultado = cursor.fetchone()
            if not resultado:
                raise Exception("Serviço não encontrado.")
            
            valor_unitario = Decimal(resultado[0]) 

            cursor.execute("SELECT COALESCE(MAX(sequencial), 0) + 1 FROM ordem_servico_servicos WHERE osv_id = %s", (osv_id,))
            sequencial = cursor.fetchone()[0]

            valor_total = valor_unitario * qtd_serv

            adicionar_servicos_na_ordem(osv_id, serv_id, qtd_serv, sequencial, valor_unitario, valor_total, ano)

            cursor.execute("""
            UPDATE ordem_servico 
                SET valor_total = (
                    COALESCE((
                        SELECT SUM(ordem_servico_produtos.valor_total) 
                        FROM ordem_servico_produtos
                        WHERE ordem_servico_produtos.osv_id = %s AND ordem_servico_produtos.ano = %s
                    ), 0) + 
                    COALESCE((
                        SELECT SUM(ordem_servico_servicos.valor_total) 
                        FROM ordem_servico_servicos
                        WHERE ordem_servico_servicos.osv_id = %s AND ordem_servico_servicos.ano = %s
                    ), 0)
                )
                WHERE ordem_servico.id = %s AND ordem_servico.ano = %s
            """, (osv_id, ano, osv_id, ano, osv_id, ano))

                    
            conexao.commit()
            cursor.close()
            conexao.close()

            atualizar_lista_servicos()
            combo_servico.set("")
            entry_qtd_serv.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Erro", str(e))


    tk.Button(frame_add, text="Adicionar Serviço", command=adicionar_servico).grid(row=0, column=4, padx=10)

    def excluir_servico():
        item = tree.selection()
        if not item:
            messagebox.showwarning("Aviso", "Selecione um serviço para excluir.")
            return

        servico_id, nome, sequencial, quantidade, valor_unitario, valor_total = tree.item(item)['values']

        if not messagebox.askyesno("Confirmação", "Deseja excluir este serviço da OS?"):
            return

        conexao = conectar()
        cursor = conexao.cursor()

        cursor.execute("""
            DELETE FROM ordem_servico_servicos
            WHERE osv_id = %s AND sequencial = %s
            and ano = %s
        """, (osv_id, int(sequencial), ano))

        cursor.execute("""
        UPDATE ordem_servico 
        SET valor_total = (
            COALESCE((
                SELECT SUM(ordem_servico_produtos.valor_total) 
                FROM ordem_servico_produtos
                WHERE ordem_servico_produtos.osv_id = %s AND ordem_servico_produtos.ano = %s
            ), 0) + 
            COALESCE((
                SELECT SUM(ordem_servico_servicos.valor_total) 
                FROM ordem_servico_servicos
                WHERE ordem_servico_servicos.osv_id = %s AND ordem_servico_servicos.ano = %s
            ), 0)
        )
        WHERE ordem_servico.id = %s AND ordem_servico.ano = %s
    """, (osv_id, ano, osv_id, ano, osv_id, ano))


        conexao.commit()
        cursor.close()
        conexao.close()

        atualizar_lista_servicos()

    tk.Button(frame_add, text="Excluir Serviço", command=excluir_servico).grid(row=1, column=0, columnspan=5, pady=10)

    atualizar_lista_servicos()


    


