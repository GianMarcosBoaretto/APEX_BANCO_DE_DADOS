import tkinter as tk
from tkinter import ttk, messagebox
from conexao import conectar

# Função para formatar como moeda (R$)
def formatar_moeda(event, entry):
    texto = entry.get().replace("R$", "").replace(".", "").replace(",", "").strip()

    # Impede que o "R$ " seja apagado
    if not entry.get().startswith("R$ "):
        entry.insert(0, "R$ ")

    # Captura apenas os números
    numeros = ''.join(filter(str.isdigit, texto))

    if not numeros:
        entry.delete(0, tk.END)
        entry.insert(0, "R$ ")
        return

    valor = int(numeros)
    formatado = f"{valor/100:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    entry.delete(0, tk.END)
    entry.insert(0, f"R$ {formatado}")

def abrir_editar_produto():
    janela = tk.Tk()
    janela.title("Editar Produtos/Serviços")
    janela.geometry("700x450")

    tk.Label(janela, text="Lista de Produtos/Serviços", font=("Arial", 12, "bold")).pack(pady=10)

    frame = tk.Frame(janela)
    frame.pack(expand=True, fill="both")

    tree = ttk.Treeview(frame, columns=("id", "nome", "custo", "valor", "quantidade", "servico"), show='headings')
    tree.heading("id", text="ID")
    tree.heading("nome", text="Nome")
    tree.heading("custo", text="Custo")
    tree.heading("valor", text="Valor")
    tree.heading("quantidade", text="Estoque")
    tree.heading("servico", text="Serviço")

    tree.column("id", width=40)
    tree.column("nome", width=200)
    tree.column("custo", width=80)
    tree.column("valor", width=80)
    tree.column("quantidade", width=80)
    tree.column("servico", width=60)

    tree.pack(expand=True, fill="both")

    def carregar_produtos():
        conexao = conectar()
        if not conexao:
            messagebox.showerror("Erro", "Erro ao conectar com o banco.")
            return
        cursor = conexao.cursor()
        cursor.execute(""" 
            SELECT id, nome, custo_compra, valor_venda, quantidade_estoque, fl_servico
            FROM produtos
            ORDER BY id DESC
        """)
        for row in cursor.fetchall():
            tree.insert("", tk.END, values=row)
        cursor.close()
        conexao.close()

    def editar_produto_selecionado():
        item = tree.focus()
        if not item:
            messagebox.showwarning("Aviso", "Selecione um produto/serviço.")
            return
        valores = tree.item(item, 'values')
        produto_id = valores[0]
        
        # Consulta para obter os dados completos do produto antes de abrir a tela de edição
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute("SELECT nome, custo_compra, valor_venda, quantidade_estoque, fl_servico, fl_inativo FROM produtos WHERE id = %s", (produto_id,))
        produto = cursor.fetchone()
        cursor.close()
        conexao.close()

        if not produto:
            messagebox.showerror("Erro", "Produto não encontrado.")
            return
        
        # Passando as informações para a tela de edição
        abrir_tela_edicao(produto_id, produto, tree)

    def voltar_para_main():
        janela.destroy()
        import main
        main.main()

    # Botões
    botoes_frame = tk.Frame(janela)
    botoes_frame.pack(pady=10)

    tk.Button(botoes_frame, text="Editar Produto/Serviço Selecionado", command=editar_produto_selecionado).pack(side="left", padx=10)
    tk.Button(botoes_frame, text="Voltar", command=voltar_para_main).pack(side="left", padx=10)

    carregar_produtos()

    janela.mainloop()

def abrir_tela_edicao(produto_id, produto, tree):
    editar_janela = tk.Toplevel()
    editar_janela.title(f"Editar Produto ID {produto_id}")
    editar_janela.geometry("400x350")

    nome_var = tk.StringVar(value=produto[0])
    custo_var = tk.StringVar(value=str(produto[1]))
    valor_var = tk.StringVar(value=str(produto[2]))
    estoque_var = tk.StringVar(value=str(produto[3]))
    servico_var = tk.BooleanVar(value=produto[4] == 1)  # Convertendo para booleano
    inativo_var = tk.BooleanVar(value=produto[5] == 1)  # Convertendo para booleano

    # Labels e Entradas
    tk.Label(editar_janela, text="Nome:").pack(anchor="w", padx=20, pady=(10, 0))
    entry_nome = tk.Entry(editar_janela, width=40, textvariable=nome_var)
    entry_nome.pack(padx=20)

    tk.Label(editar_janela, text="Custo de Compra:").pack(anchor="w", padx=20, pady=(10, 0))
    entry_custo = tk.Entry(editar_janela, width=20, textvariable=custo_var)
    entry_custo.pack(padx=20)
    entry_custo.bind("<KeyRelease>", lambda e: formatar_moeda(e, entry_custo))

    tk.Label(editar_janela, text="Valor de Venda:").pack(anchor="w", padx=20, pady=(10, 0))
    entry_valor = tk.Entry(editar_janela, width=20, textvariable=valor_var)
    entry_valor.pack(padx=20)
    entry_valor.bind("<KeyRelease>", lambda e: formatar_moeda(e, entry_valor))

    tk.Label(editar_janela, text="Quantidade em Estoque:").pack(anchor="w", padx=20, pady=(10, 0))
    entry_estoque = tk.Entry(editar_janela, width=10, textvariable=estoque_var)
    entry_estoque.pack(padx=20)

    # Modificando o Checkbutton de Serviço
    tk.Checkbutton(editar_janela, text="Serviço", variable=servico_var,state="disabled").pack(anchor="w", padx=20)

    tk.Checkbutton(editar_janela, text="Inativar", variable=inativo_var).pack(anchor="w", padx=20)

    def salvar():
        try:
            conexao = conectar()
            cursor = conexao.cursor()
            cursor.execute(""" 
                UPDATE produtos
                SET nome = %s, custo_compra = %s, valor_venda = %s, quantidade_estoque = %s, fl_inativo = %s
                WHERE id = %s
            """, (
                nome_var.get(),
                float(custo_var.get().replace("R$", "").replace(",", ".")),
                float(valor_var.get().replace("R$", "").replace(",", ".")),
                int(estoque_var.get()),
                1 if inativo_var.get() else 0,
                produto_id
            ))
            conexao.commit()
            cursor.close()
            conexao.close()
            messagebox.showinfo("Sucesso", "Produto atualizado com sucesso.")

            # Refresh na Treeview
            for i in tree.get_children():
                tree.delete(i)
            
            nova_conexao = conectar()
            novo_cursor = nova_conexao.cursor()
            novo_cursor.execute(""" 
                SELECT id, nome, custo_compra, valor_venda, quantidade_estoque, fl_servico
                FROM produtos
                ORDER BY id DESC
            """)
            for row in novo_cursor.fetchall():
                tree.insert("", tk.END, values=row)
            novo_cursor.close()
            nova_conexao.close()

            editar_janela.destroy()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar: {e}")

    tk.Button(editar_janela, text="Salvar Alterações", command=salvar).pack(pady=15)
