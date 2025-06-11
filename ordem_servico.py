import tkinter as tk
from tkinter import ttk, messagebox
from conexao import conectar
import main
import datetime  # Para pegar o ano atual

def buscar_clientes():
    conexao = conectar()
    clientes = []
    if conexao:
        cursor = conexao.cursor()
        try:
            cursor.execute("SELECT id, nome FROM clientes ORDER BY nome")
            clientes = cursor.fetchall()
        except Exception as erro:
            print("Erro ao buscar clientes:", erro)
        finally:
            cursor.close()
            conexao.close()
    return clientes

# Função para buscar o último ID do ano
def buscar_ultimo_id_ano(ano):
    conexao = conectar()
    ultimo_id = None
    if conexao:
        cursor = conexao.cursor()
        try:
            cursor.execute("SELECT MAX(id) FROM ordem_servico WHERE ano = %s", (ano,))
            resultado = cursor.fetchone()
            if resultado[0]:
                ultimo_id = resultado[0]
        except Exception as erro:
            print("Erro ao buscar último ID do ano:", erro)
        finally:
            cursor.close()
            conexao.close()
    return ultimo_id

def salvar_ordem_servico(cliente_id, data_cadastro, modelo, descricao, observacao, ano):
    # Busca o último ID para o ano atual
    ultimo_id = buscar_ultimo_id_ano(ano)
    
    if ultimo_id is None:
        novo_id = "0001"  # Caso não haja nenhuma ordem de serviço para o ano, começa do ID 'ano0001'
    else:
        novo_id = str(int(ultimo_id) + 1)  # Incrementa 1 no último ID encontrado
    
    conexao = conectar()
    if conexao:
        cursor = conexao.cursor()
        try:
            sql = """
            INSERT INTO ordem_servico (id, cliente_id, data_cadastro, modelo, descricao, observacao, ano, valor_total)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            valores = (novo_id, cliente_id, data_cadastro, modelo, descricao, observacao, ano, 0)
            cursor.execute(sql, valores)
            conexao.commit()
            print("Ordem de serviço salva com sucesso!")
            limpar_campos()
        except Exception as erro:
            print("Erro ao salvar ordem de serviço:", erro)
        finally:
            cursor.close()
            conexao.close()

def abrir_cadastro_ordem_servico():
    clientes = buscar_clientes()
    nomes_clientes = [cli[1] for cli in clientes]

    janela = tk.Tk()
    janela.title("Cadastro de Ordem de Serviço")
    janela.geometry("450x400")
    janela.resizable(False, False)

    def voltar_para_main():
        janela.destroy()
        main.main()

    def salvar_dados():
        cliente_nome = combo_cliente.get()
        data = entry_data.get().strip()
        modelo = entry_modelo.get()
        descricao = entry_descricao.get("1.0", tk.END).strip()
        observacao = entry_observacao.get("1.0", tk.END).strip()

        if not cliente_nome or not data or not modelo or not descricao:
            messagebox.showwarning("Atenção", "Preencha todos os campos obrigatórios.")
            return

        cliente_id = next((cli[0] for cli in clientes if cli[1] == cliente_nome), None)
        if cliente_id is None:
            messagebox.showerror("Erro", "Cliente inválido.")
            return
        
        try:
            data_convertida = datetime.datetime.strptime(data, "%d-%m-%Y").strftime("%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Erro", "Data inválida. Use o formato DD-MM-AAAA.")
            return
        
        # Captura o ano atual
        ano_atual = datetime.datetime.now().year

        # Salva a ordem de serviço com o ID baseado no último ID do ano
        salvar_ordem_servico(cliente_id, data_convertida, modelo, descricao, observacao, ano_atual)
        messagebox.showinfo("Sucesso", "Ordem de serviço cadastrada.")
        limpar_campos()

    # Função para limpar todos os campos
    def limpar_campos():
        entry_data.delete(0, tk.END)
        entry_modelo.delete(0, tk.END)
        entry_observacao.delete(1.0, tk.END)
        entry_descricao.delete(1.0, tk.END)
        combo_cliente.set('')    

    # Layout
    tk.Label(janela, text="Cliente:").pack(anchor="w", padx=20, pady=(10, 0))
    combo_cliente = ttk.Combobox(janela, values=nomes_clientes, state="readonly", width=50)
    combo_cliente.pack(padx=20)

    tk.Label(janela, text="Data de Cadastro (DD-MM-AAAA):").pack(anchor="w", padx=20, pady=(10, 0))
    entry_data = tk.Entry(janela, width=30)
    entry_data.pack(padx=20)

    tk.Label(janela, text="Modelo:").pack(anchor="w", padx=20, pady=(10, 0))
    entry_modelo = tk.Entry(janela, width=50)
    entry_modelo.pack(padx=20)

    tk.Label(janela, text="Descrição:").pack(anchor="w", padx=20, pady=(10, 0))
    entry_descricao = tk.Text(janela, height=3, width=50)
    entry_descricao.pack(padx=20)

    tk.Label(janela, text="Observação:").pack(anchor="w", padx=20, pady=(10, 0))
    entry_observacao = tk.Text(janela, height=3, width=50)
    entry_observacao.pack(padx=20)

    # Frame para os botões
    frame_botoes = tk.Frame(janela)
    frame_botoes.pack(pady=(10, 20))

    # Botão Salvar
    tk.Button(frame_botoes, text="Salvar Ordem de Serviço", command=salvar_dados).pack(side="left", padx=10)

    # Botão Voltar
    tk.Button(frame_botoes, text="Voltar", command=voltar_para_main).pack(side="left", padx=10)

    janela.mainloop()
