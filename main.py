import tkinter as tk
from tkinter import ttk
import cidades
import clientes
import ordem_servico
import produtos
import os_editar 
import editar_produto
import editar_cliente
import editar_cidade
import usuarios


def main():
    janela = tk.Tk()
    janela.title("Sistema de Cadastros")
    janela.geometry("800x600")
    janela.resizable(False, False)

    tk.Label(janela, text="Menu Principal", font=("Arial", 16, "bold")).pack(pady=20)

    # Funções locais para fechar a janela e abrir as telas
    def abrir_clientes():
        janela.destroy()
        clientes.abrir_cadastro_clientes()

    def abrir_produtos():
        janela.destroy()
        produtos.abrir_cadastro_produtos()

    def abrir_ordem_servico():
        janela.destroy()
        ordem_servico.abrir_cadastro_ordem_servico()

    def abrir_cidades():
        janela.destroy()
        cidades.abrir_cadastro_cidades()

    def abrir_usuarios():
        usuarios.janela_principal()
            
    def abrir_osv():
        janela.destroy()
        os_editar.abrir_seletor_ordens()

    def editar_produtos():
        janela.destroy()
        editar_produto.abrir_editar_produto()      

    def editar_clientes():
        janela.destroy()
        editar_cliente.abrir_edicao_cliente()

    def editar_cidades():
        janela.destroy()
        editar_cidade.abrir_edicao_cidade()


    # Criar o Notebook (aqui vai ter as abas)
    notebook = ttk.Notebook(janela)
    notebook.pack(expand=True, fill="both", padx=10, pady=10)

    # Criar as abas
    aba_cadastros = ttk.Frame(notebook)
    aba_edicoes = ttk.Frame(notebook)

    notebook.add(aba_cadastros, text="Cadastros")
    notebook.add(aba_edicoes, text="Edições")

    # Adicionar botões na aba de Cadastros
    tk.Button(aba_cadastros, text="Cadastro de Clientes", width=30, command=abrir_clientes).pack(pady=5)
    tk.Button(aba_cadastros, text="Cadastro de Produtos", width=30, command=abrir_produtos).pack(pady=5)
    tk.Button(aba_cadastros, text="Cadastro de Ordem de Serviço", width=30, command=abrir_ordem_servico).pack(pady=5)
    tk.Button(aba_cadastros, text="Cadastro de Cidades", width=30, command=abrir_cidades).pack(pady=5)
    tk.Button(aba_cadastros, text="Gerenciamento de Usuários", width=30, command=abrir_usuarios).pack(pady=5)

    # Adicionar botões na aba de Edições
    tk.Button(aba_edicoes, text="Editar OSV", width=30, command=abrir_osv).pack(pady=5) 
    tk.Button(aba_edicoes, text="Editar Produtos", width=30, command=editar_produtos).pack(pady=5) 
    tk.Button(aba_edicoes, text="Editar Cliente", width=30, command=editar_clientes).pack(pady=5) 
    tk.Button(aba_edicoes, text="Editar Cidades", width=30, command=editar_cidades).pack(pady=5) 

    janela.mainloop()


if __name__ == '__main__':
    main()
