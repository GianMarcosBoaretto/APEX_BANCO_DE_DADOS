import tkinter as tk
from tkinter import ttk, messagebox
from conexao import conectar
from os_edicao import abrir_edicao_ordem_servico
import main

def abrir_seletor_ordens():
    janela = tk.Tk()
    janela.title("Selecionar Ordem de Serviço")
    janela.geometry("500x400")

    tk.Label(janela, text="Selecione uma Ordem de Serviço", font=("Arial", 12, "bold")).pack(pady=10)

    frame = tk.Frame(janela)
    frame.pack(expand=True, fill="both")

    tree = ttk.Treeview(frame, columns=("id", "ano", "nome_cliente", "data_cadastro"), show='headings')
    tree.heading("id", text="ID")
    tree.heading("ano", text="Ano")
    tree.heading("nome_cliente", text="Cliente")
    tree.heading("data_cadastro", text="Data")
    tree.pack(expand=True, fill="both")

    def carregar_ordens():
        conexao = conectar()
        if not conexao:
            messagebox.showerror("Erro", "Erro ao conectar com o banco.")
            return
        cursor = conexao.cursor()
        cursor.execute("""
            SELECT os.id, os.ano, c.nome, os.data_cadastro
            FROM ordem_servico os
            JOIN clientes c ON os.cliente_id = c.id
            ORDER BY os.id DESC
        """)
        for row in cursor.fetchall():
            tree.insert("", tk.END, values=row)
        cursor.close()
        conexao.close()

    def editar_os_selecionada():
        item = tree.focus()
        if not item:
            messagebox.showwarning("Aviso", "Selecione uma OS.")
            return
        osv_id = tree.item(item, 'values')[0]
        ano = tree.item(item, 'values') [1]
        abrir_edicao_ordem_servico(osv_id, ano)
        janela.destroy()
    
    # Função de Retorno do main
    def voltar_para_main():
        janela.destroy()
        main.main()

    # Botões
    botoes_frame = tk.Frame(janela)
    botoes_frame.pack(pady=10)

    tk.Button(botoes_frame, text="Editar Selecionada", command=editar_os_selecionada).pack(side="left", padx=10)
    carregar_ordens()

    tk.Button(botoes_frame, text="Voltar ao Menu-Principal", command=voltar_para_main).pack(side="left", padx=10)

    janela.mainloop()

if __name__ == "__main__":
    abrir_seletor_ordens()