import tkinter as tk
from tkinter import messagebox
from conexao import conectar
import main

# Função para salvar no Banco de Dados
def salvar_produtos(nome, custo, valor, quantidade, servico):
    conexao = conectar()
    if conexao:
        cursor = conexao.cursor()
        try:
            sql = "INSERT INTO produtos (nome, custo_compra, valor_venda, quantidade_estoque, fl_servico) VALUES (%s, %s, %s, %s, %s)"
            valores = (nome, custo, valor, quantidade, servico)
            cursor.execute(sql, valores)
            conexao.commit()
            print("Produto salvo com sucesso!")
        except Exception as erro:
            print("Erro ao salvar produto:", erro)
        finally:
            cursor.close()
            conexao.close()

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

# Função Principal
def abrir_cadastro_produtos():
    janela = tk.Tk()
    janela.title("Cadastro de Produtos")
    janela.geometry("400x300")
    janela.resizable(False, False)

    servico_var = tk.BooleanVar()

    # Função de Salvar dados
    def salvar_dados_produtos():
        nome = entry_nome.get()
        custo = entry_custo.get().replace("R$", "").replace(".", "").replace(",", ".").strip()
        valor = entry_valor.get().replace("R$", "").replace(".", "").replace(",", ".").strip()
        quantidade = entry_estoque.get()
        servico = 1 if servico_var.get() else 0

        if (not nome or not custo or not valor or not quantidade) and servico == 0:
            messagebox.showwarning("Atenção", "Preencha todos os campos corretamente.")
            return
        
        if (not nome or not valor) and servico == 1:
            messagebox.showwarning("Atenção", "Preencha todos os campos corretamente.")
            return

        if servico == 0:
            try:
                custo = float(custo)
                valor = float(valor)
                quantidade = int(quantidade)
            except ValueError:
                messagebox.showerror("Erro", "Certifique-se de que custo, valor e quantidade estão corretos.")
                return
            
        if servico == 1:
            try:
                custo = 0.00
                valor = float(valor)
                quantidade = 0
            except ValueError:
                messagebox.showerror("Erro", "Certifique-se de que valor de venda esteje correto.")
                return            

        salvar_produtos(nome, custo, valor, quantidade, servico)
        messagebox.showinfo("Sucesso", "Produto/Serviço salvo com sucesso!")
        limpar_campos()

         # Função para limpar todos os campos
    def limpar_campos():
        entry_nome.delete(0, tk.END)
        entry_custo.delete(0, tk.END)
        entry_valor.delete(0, tk.END)
        entry_estoque.delete(0, tk.END)
        servico_var.set(False)  # Desmarca o checkbox

    # Função de Retorno do main
    def voltar_para_main():
        janela.destroy()
        main.main()

    # Labels e entradas
    tk.Label(janela, text="Nome:").pack(anchor="w", padx=20, pady=(10, 0))
    entry_nome = tk.Entry(janela, width=40)
    entry_nome.pack(padx=20)

    tk.Label(janela, text="Custo de Compra:").pack(anchor="w", padx=20, pady=(10, 0))
    entry_custo = tk.Entry(janela, width=20)
    entry_custo.pack(padx=20)
    entry_custo.bind("<KeyRelease>", lambda e: formatar_moeda(e, entry_custo))

    tk.Label(janela, text="Valor de Venda:").pack(anchor="w", padx=20, pady=(10, 0))
    entry_valor = tk.Entry(janela, width=20)
    entry_valor.pack(padx=20)
    entry_valor.bind("<KeyRelease>", lambda e: formatar_moeda(e, entry_valor))

    tk.Label(janela, text="Quantidade em Estoque:").pack(anchor="w", padx=20, pady=(10, 0))
    entry_estoque = tk.Entry(janela, width=10)
    entry_estoque.pack(padx=20)

    tk.Checkbutton(janela, text="Serviço", variable=servico_var).pack(anchor="w", padx=20)

    # Frame para os botões
    frame_botoes = tk.Frame(janela)
    frame_botoes.pack(pady=(10, 20))

    # Botão Salvar
    tk.Button(frame_botoes, text="Salvar Produto/Serviço", command=salvar_dados_produtos).pack(side="left", padx=10)

    # Botão Voltar
    tk.Button(frame_botoes, text="Voltar", command=voltar_para_main).pack(side="left", padx=10)

    janela.mainloop()
