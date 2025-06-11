import tkinter as tk
from tkinter import messagebox, ttk
from conexao import conectar
import main

# Função para buscar todos os clientes
def buscar_todos_clientes():
    conexao = conectar()
    clientes = []
    if conexao:
        cursor = conexao.cursor()
        try:
            cursor.execute("SELECT id, nome, cpf, telefone, cidade_id FROM clientes ORDER BY nome")
            clientes = cursor.fetchall()
        except Exception as erro:
            print("Erro ao buscar clientes:", erro)
        finally:
            cursor.close()
            conexao.close()
    return clientes

# Função para buscar as cidades do banco de dados
def buscar_cidades():
    conexao = conectar()
    cidades = []
    if conexao:
        cursor = conexao.cursor()
        try:
            cursor.execute("SELECT id, nome FROM cidades ORDER BY nome")
            cidades = cursor.fetchall()
        except Exception as erro:
            print("Erro ao buscar cidades:", erro)
        finally:
            cursor.close()
            conexao.close()
    return cidades

# Função para buscar um cliente pelo id
def buscar_cliente_por_id(id_cliente):
    conexao = conectar()
    cliente = None
    if conexao:
        cursor = conexao.cursor()
        try:
            cursor.execute("SELECT nome, cpf, cidade_id, telefone FROM clientes WHERE id = %s", (id_cliente,))
            cliente = cursor.fetchone()
        except Exception as erro:
            print("Erro ao buscar cliente:", erro)
        finally:
            cursor.close()
            conexao.close()
    return cliente

# Função para salvar no banco de dados
def salvar_cliente(id_cliente, nome, cpf, cidade_id, telefone):
    conexao = conectar()
    if conexao:
        cursor = conexao.cursor()
        try:
            sql = "UPDATE clientes SET nome = %s, cpf = %s, cidade_id = %s, telefone = %s WHERE id = %s"
            valores = (nome, cpf, cidade_id, telefone, id_cliente)
            cursor.execute(sql, valores)
            conexao.commit()
            print("Cliente atualizado com sucesso!")
        except Exception as erro:
            print("Erro ao salvar cliente:", erro)
        finally:
            cursor.close()
            conexao.close()

# Função para abrir a tela de edição de cliente
def abrir_edicao_cliente():
    cidades = buscar_cidades()
    nomes_cidades = [cid[1] for cid in cidades]

    # Tela de edição de cliente
    janela = tk.Tk()
    janela.title("Edição de Cliente")
    janela.geometry("700x450")

    # Listar todos os clientes
    tk.Label(janela, text="Clientes", font=("Arial", 12, "bold")).pack(pady=10)

    frame = tk.Frame(janela)
    frame.pack(expand=True, fill="both")

    tree = ttk.Treeview(frame, columns=("id", "nome", "cpf", "telefone", "cidade"), show='headings')
    tree.heading("id", text="ID")
    tree.heading("nome", text="Nome")
    tree.heading("cpf", text="CPF")
    tree.heading("telefone", text="Telefone")
    tree.heading("cidade", text="Cidade")

    tree.column("id", width=40)
    tree.column("nome", width=200)
    tree.column("cpf", width=120)
    tree.column("telefone", width=120)
    tree.column("cidade", width=150)

    tree.pack(expand=True, fill="both")

    def voltar_para_main():
        janela.destroy()
        main.main()

    # Carregar os clientes na árvore
    def carregar_clientes():
        clientes = buscar_todos_clientes()
        for cliente in clientes:
            cidade_nome = next((cid[1] for cid in cidades if cid[0] == cliente[4]), "Cidade não encontrada")
            tree.insert("", tk.END, values=(cliente[0], cliente[1], cliente[2], cliente[3], cidade_nome))

    # Função para editar o cliente selecionado
    def editar_cliente_selecionado():
        item = tree.focus()
        if not item:
            messagebox.showwarning("Aviso", "Selecione um cliente.")
            return
        valores = tree.item(item, 'values')
        cliente_id = valores[0]

        cliente = buscar_cliente_por_id(cliente_id)
        if cliente:
            abrir_tela_edicao(cliente_id, cliente, tree)

    # Botões
    botoes_frame = tk.Frame(janela)
    botoes_frame.pack(pady=10)

    tk.Button(botoes_frame, text="Editar Cliente", command=editar_cliente_selecionado).pack(side="left", padx=10)
    tk.Button(botoes_frame, text="Voltar", command=voltar_para_main).pack(side="left", padx=10)

    carregar_clientes()

    janela.mainloop()

# Função para abrir a tela de edição de cliente com os dados
def abrir_tela_edicao(id_cliente, cliente, tree):
    cidades = buscar_cidades()
    nomes_cidades = [cid[1] for cid in cidades]

    janela_edicao = tk.Tk()
    janela_edicao.title("Editar Cliente")
    janela_edicao.geometry("400x350")
    janela_edicao.resizable(False, False)

    # Função para formatar e validar CPF
    def formatar_cpf(event=None):
        cpf = entry_cpf.get().replace(".", "").replace("-", "")
        if not cpf.isdigit():
            return
        if len(cpf) > 11:
            cpf = cpf[:11]
        formatado = ''
        if len(cpf) >= 3:
            formatado += cpf[:3] + '.'
        if len(cpf) >= 6:
            formatado += cpf[3:6] + '.'
        if len(cpf) >= 9:
            formatado += cpf[6:9] + '-'
        if len(cpf) > 9:
            formatado += cpf[9:]
        elif len(cpf) > 6:
            formatado += cpf[6:]
        elif len(cpf) > 3:
            formatado += cpf[3:]
        else:
            formatado += cpf
        entry_cpf.delete(0, tk.END)
        entry_cpf.insert(0, formatado)

    # Função para formatar o telefone
    def formatar_telefone(event=None):
        # Salva a posição atual do cursor
        posicao = entry_tel.index(tk.INSERT)

        # Captura apenas números
        telefone = entry_tel.get()
        numeros = ''.join(filter(str.isdigit, telefone))

        # Se tiver menos de 3 dígitos, não formata ainda
        if len(numeros) < 3:
            return

        # Limita a 11 dígitos
        if len(numeros) > 11:
            numeros = numeros[:11]

        # Começa a formatação
        formatado = f"({numeros[:2]})"

        if len(numeros) >= 7:
            formatado += f"{numeros[2:7]}-{numeros[7:]}"
        elif len(numeros) > 2:
            formatado += numeros[2:]

        # Atualiza o campo
        entry_tel.delete(0, tk.END)
        entry_tel.insert(0, formatado)

        # Calcula nova posição com base na quantidade de dígitos
        digitos_digitados = len(numeros)

        # Mapeamento de posição bruta (sem máscara) para posição formatada
        if digitos_digitados <= 2:
            nova_pos = digitos_digitados + 1  # após o (
        elif digitos_digitados <= 7:
            nova_pos = digitos_digitados + 2  # +2 por conta do "(" e ")"
        else:
            nova_pos = digitos_digitados + 3  # +3 por "()" e "-"

        # Reposiciona o cursor corretamente
        entry_tel.icursor(nova_pos)


    # Labels e entradas para editar os dados do cliente
    tk.Label(janela_edicao, text="Nome:").pack(anchor="w", padx=20, pady=(10, 0))
    entry_nome = tk.Entry(janela_edicao, width=40)
    entry_nome.pack(padx=20)
    entry_nome.insert(0, cliente[0])

    tk.Label(janela_edicao, text="CPF:").pack(anchor="w", padx=20, pady=(10, 0))
    entry_cpf = tk.Entry(janela_edicao, width=40)
    entry_cpf.pack(padx=20)
    entry_cpf.insert(0, cliente[1])
    entry_cpf.bind("<KeyRelease>", formatar_cpf)
    formatar_cpf()

    tk.Label(janela_edicao, text="Telefone:").pack(anchor="w", padx=20, pady=(10, 0))
    entry_tel = tk.Entry(janela_edicao, width=40)
    entry_tel.pack(padx=20)
    entry_tel.insert(0, cliente[3])
    entry_tel.bind("<KeyRelease>", formatar_telefone)
    formatar_telefone()

    tk.Label(janela_edicao, text="Cidade:").pack(anchor="w", padx=20, pady=(10, 0))
    combo_cidade = ttk.Combobox(janela_edicao, values=nomes_cidades, state="readonly", width=37)
    combo_cidade.pack(padx=20)
    combo_cidade.set(next(cidade[1] for cidade in cidades if cidade[0] == cliente[2]))

    
    def salvar_dados_cliente():
        nome = entry_nome.get()
        cpf = entry_cpf.get().replace(".", "").replace("-", "")
        cidade_nome = combo_cidade.get()
        telefone = entry_tel.get().replace("(", "").replace(")", "").replace("-", "").replace(" ", "")

        if not nome or not cpf or not cidade_nome or not telefone:
            messagebox.showwarning("Atenção", "Preencha todos os campos corretamente.")
            return

        if len(cpf) != 11:
            messagebox.showerror("Erro", "CPF deve conter 11 dígitos.")
            return

        if len(telefone) not in [10, 11]:
            messagebox.showerror("Erro", "Telefone deve conter 10 ou 11 dígitos.")
            return

        cidade_id = next((cid[0] for cid in cidades if cid[1] == cidade_nome), None)
        if cidade_id is None:
            messagebox.showerror("Erro", "Cidade inválida.")
            return

        salvar_cliente(id_cliente, nome, cpf, cidade_id, telefone)
        messagebox.showinfo("Sucesso", "Cliente atualizado com sucesso!")

        janela_edicao.destroy()

        # 🔄 Refresh na tree
        for item in tree.get_children():
            tree.delete(item)
        clientes = buscar_todos_clientes()
        for cliente in clientes:
            tree.insert("", "end", values=cliente)

    # Botão salvar
    tk.Button(janela_edicao, text="Salvar Alterações", command=salvar_dados_cliente).pack(pady=10)


    janela_edicao.mainloop()
