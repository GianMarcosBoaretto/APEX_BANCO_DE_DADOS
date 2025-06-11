import tkinter as tk
from tkinter import messagebox, ttk
from conexao import conectar
import main

# Função para buscar todas as cidades
def buscar_cidades():
    conexao = conectar()
    cidades = []
    if conexao:
        cursor = conexao.cursor()
        try:
            cursor.execute("SELECT id, nome, uf FROM cidades ORDER BY nome")
            cidades = cursor.fetchall()
        except Exception as erro:
            print("Erro ao buscar cidades:", erro)
        finally:
            cursor.close()
            conexao.close()
    return cidades

# Função para salvar a cidade no banco de dados
def salvar_cidade(id_cidade, nome, uf):
    conexao = conectar()
    if conexao:
        cursor = conexao.cursor()
        try:
            sql = "UPDATE cidades SET nome = %s, uf = %s WHERE id = %s"
            valores = (nome, uf, id_cidade)  # Corrigido para passar o 'uf'
            cursor.execute(sql, valores)
            conexao.commit()
            print("Cidade atualizada com sucesso!")
        except Exception as erro:
            print("Erro ao salvar cidade:", erro)
        finally:
            cursor.close()
            conexao.close()

# Função para abrir a tela de edição de cidade
def abrir_edicao_cidade():
    cidades = buscar_cidades()

    # Tela de edição de cidade
    janela = tk.Tk()
    janela.title("Edição de Cidade")
    janela.geometry("700x450")

    # Listar todas as cidades
    tk.Label(janela, text="Cidades", font=("Arial", 12, "bold")).pack(pady=10)

    frame = tk.Frame(janela)
    frame.pack(expand=True, fill="both")

    tree = ttk.Treeview(frame, columns=("id", "nome", "uf"), show='headings')  # Adicionando "uf"
    tree.heading("id", text="ID")
    tree.heading("nome", text="Nome")
    tree.heading("uf", text="UF")  # Adicionando a coluna UF

    tree.column("id", width=40)
    tree.column("nome", width=200)
    tree.column("uf", width=80)  # Ajuste de largura para a coluna UF

    tree.pack(expand=True, fill="both")

    def voltar_para_main():
        janela.destroy()
        main.main()

    # Carregar as cidades na árvore
    def carregar_cidades():
        for item in tree.get_children():
            tree.delete(item)
        cidades_atualizadas = buscar_cidades()
        for cidade in cidades_atualizadas:
            tree.insert("", tk.END, values=(cidade[0], cidade[1], cidade[2]))

    # Função para editar a cidade selecionada
    def editar_cidade_selecionada():
        item = tree.focus()
        if not item:
            messagebox.showwarning("Aviso", "Selecione uma cidade.")
            return
        valores = tree.item(item, 'values')
        cidade_id = valores[0]

        print(f"ID da cidade selecionada: {cidade_id}")  # Depuração - Verificando o ID da cidade selecionada

        # Verifique se o id da cidade está correto e obtenha o nome e o UF
        cidade_nome = valores[1]
        uf = valores[2]

        if cidade_nome:
            print(f"Cidade encontrada: {cidade_nome}")  # Depuração - Verificando a cidade encontrada
            # Abrir a tela de edição da cidade com o nome encontrado
            abrir_tela_edicao(cidade_id, (cidade_id, cidade_nome, uf), carregar_cidades)
        else:
            messagebox.showwarning("Aviso", "Cidade não encontrada")

    # Botões
    botoes_frame = tk.Frame(janela)
    botoes_frame.pack(pady=10)
    # Botão para editar a cidade selecionada
    tk.Button(botoes_frame, text="Editar Cidade", command=editar_cidade_selecionada).pack(side="left", padx=10)
    tk.Button(botoes_frame, text="Voltar", command=voltar_para_main).pack(side="left", padx=10)

    carregar_cidades()

    janela.mainloop()

# Função para abrir a tela de edição de cidade com os dados
def abrir_tela_edicao(id_cidade, cidade, callback_recarregar):
    janela_edicao = tk.Tk()
    janela_edicao.title("Editar Cidade")
    janela_edicao.geometry("400x250")
    janela_edicao.resizable(False, False)

    # Labels e entradas para editar os dados da cidade
    tk.Label(janela_edicao, text="Nome da Cidade:").pack(anchor="w", padx=20, pady=(10, 0))
    entry_nome = tk.Entry(janela_edicao, width=40)
    entry_nome.pack(padx=20)
    entry_nome.insert(0, cidade[1])

    # Labels e entradas para editar o UF da cidade
    tk.Label(janela_edicao, text="UF:").pack(anchor="w", padx=20, pady=(10, 0))
    entry_uf = tk.Entry(janela_edicao, width=40)
    entry_uf.pack(padx=20)
    entry_uf.insert(0, cidade[2])  # Inserir o valor do UF

    # Função para salvar as alterações
    def salvar_dados_cidade():
        nome = entry_nome.get()
        uf = entry_uf.get()

        if not nome or not uf:
            messagebox.showwarning("Atenção", "Preencha todos os campos corretamente.")
            return

        salvar_cidade(id_cidade, nome, uf)  # Passando 'uf' também
        messagebox.showinfo("Sucesso", "Cidade atualizada com sucesso!")
        janela_edicao.destroy()
        callback_recarregar()  # Atualiza a lista na tela principal

    # Botão salvar
    tk.Button(janela_edicao, text="Salvar Alterações", command=salvar_dados_cidade).pack(pady=10)

    janela_edicao.mainloop()
