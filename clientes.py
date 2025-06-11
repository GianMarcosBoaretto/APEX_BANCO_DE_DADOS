import tkinter as tk
from tkinter import messagebox, ttk
from conexao import conectar
import subprocess
import main

# Função para obter as cidades do banco de dados
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

# Função para salvar no Banco de Dados
def salvar_cliente(nome, cpf, cidade_id, telefone):
    conexao = conectar()
    if conexao:
        cursor = conexao.cursor()
        try:
            sql = "INSERT INTO clientes (nome, cpf, cidade_id, telefone) VALUES (%s, %s, %s, %s)"
            valores = (nome, cpf, cidade_id, telefone)
            cursor.execute(sql, valores)
            conexao.commit()
            print("Cliente salvo com sucesso!")
        except Exception as erro:
            print("Erro ao salvar cliente:", erro)
        finally:
            cursor.close()
            conexao.close()

def abrir_cadastro_clientes():
    cidades = buscar_cidades()
    nomes_cidades = [cid[1] for cid in cidades]

    janela = tk.Tk()
    janela.title("Cadastro de Clientes")
    janela.geometry("400x300")
    janela.resizable(False, False)

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

    def voltar_para_main():
        janela.destroy()
        main.main()

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

    # Função para limpar todos os campos
    def limpar_campos():
        entry_nome.delete(0, tk.END)
        entry_cpf.delete(0, tk.END)
        combo_cidade.set('')
        entry_tel.delete(0, tk.END)
        

    # Função para salvar (tratando os dados antes de enviar ao banco)
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

        salvar_cliente(nome, cpf, cidade_id, telefone)
        messagebox.showinfo("Sucesso", "Cliente salvo com sucesso!")
        limpar_campos()

    # Labels e entradas
    tk.Label(janela, text="Nome:").pack(anchor="w", padx=20, pady=(10, 0))
    entry_nome = tk.Entry(janela, width=40)
    entry_nome.pack(padx=20)

    tk.Label(janela, text="CPF:").pack(anchor="w", padx=20, pady=(10, 0))
    entry_cpf = tk.Entry(janela, width=20)
    entry_cpf.pack(padx=20)
    entry_cpf.bind("<KeyRelease>", formatar_cpf)

    tk.Label(janela, text="Cidade:").pack(anchor="w", padx=20, pady=(10, 0))
    combo_cidade = ttk.Combobox(janela, values=nomes_cidades, state="readonly", width=37)
    combo_cidade.pack(padx=20)

    tk.Label(janela, text="Telefone:").pack(anchor="w", padx=20, pady=(10, 0))
    entry_tel = tk.Entry(janela, width=40)
    entry_tel.pack(padx=20)
    entry_tel.bind("<KeyRelease>", formatar_telefone)
    
    # Frame para os botões
    frame_botoes = tk.Frame(janela)
    frame_botoes.pack(pady=(10, 20))

    # Botão Salvar
    tk.Button(frame_botoes, text="Salvar Ordem de Serviço", command=salvar_dados_cliente).pack(side="left", padx=10)

    # Botão Voltar
    tk.Button(frame_botoes, text="Voltar", command=voltar_para_main).pack(side="left", padx=10)


    janela.mainloop()
