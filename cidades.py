import tkinter as tk
from tkinter import messagebox
from conexao import conectar
import main

# Função para salvar no Banco de Dados
def salvar_cidade(nome, uf):
    conexao = conectar()
    if conexao:
        cursor = conexao.cursor()
        try:
            sql = "INSERT INTO cidades (nome, uf) VALUES (%s, %s)"
            valores = (nome, uf)
            cursor.execute(sql, valores)
            conexao.commit()
            print("Cidade salvo com sucesso!")
        except Exception as erro:
            print("Erro ao salvar cidades:", erro)
        finally:
            cursor.close()
            conexao.close()

# Função Principal
def abrir_cadastro_cidades():
    janela = tk.Tk()
    janela.title("Cadastro de Clientes")
    janela.geometry("400x300")
    janela.resizable(False, False)

    # Função de Retorno do main
    def voltar_para_main():
        janela.destroy()
        main.main()

    # Função para salvar (variáveis antes de mandar pro banco)
    def salvar_dados_cidade():
        nome = entry_nome.get()
        uf = entry_uf.get()

        if not nome or not uf:
            messagebox.showwarning("Atenção", "Preencha todos os campos corretamente.")
            return

        # Aqui você pode salvar no banco de dados, etc.
        salvar_cidade(nome, uf)
        limpar_campos()
        messagebox.showinfo("Sucesso","Cidade Salva com Sucesso.")
        

    # Função para limpar todos os campos
    def limpar_campos():
        entry_nome.delete(0, tk.END)
        entry_uf.delete(0, tk.END) 

    # Labels e entradas
    tk.Label(janela, text="Cidade:").pack(anchor="w", padx=20, pady=(10, 0))
    entry_nome = tk.Entry(janela, width=40)
    entry_nome.pack(padx=20)

    tk.Label(janela, text="UF:").pack(anchor="w", padx=20, pady=(10, 0))
    entry_uf = tk.Entry(janela, width=2)
    entry_uf.pack(padx=2)

    # Frame para os botões
    frame_botoes = tk.Frame(janela)
    frame_botoes.pack(pady=(10, 20))

    # Botão Salvar
    tk.Button(frame_botoes, text="Salvar Cidade", command=salvar_dados_cidade).pack(side="left", padx=10)

    # Botão Voltar
    tk.Button(frame_botoes, text="Voltar", command=voltar_para_main).pack(side="left", padx=10)

    janela.mainloop()

