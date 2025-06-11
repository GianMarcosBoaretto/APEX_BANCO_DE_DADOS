import tkinter as tk
from tkinter import messagebox
from tkinter import ttk  # Importando corretamente o ttk
from conexao import conectar  # Função de conexão com o banco de dados
import bcrypt  # Para hashing de senhas


def listar_usuarios(treeview):
    # Limpa a lista antes de preencher novamente
    for item in treeview.get_children():
        treeview.delete(item)
    
    conexao = conectar()
    if conexao:
        try:
            cursor = conexao.cursor()
            cursor.execute("SELECT id, usuario FROM usuarios")
            usuarios = cursor.fetchall()
            
            for usuario in usuarios:
                treeview.insert("", "end", values=(usuario[0], usuario[1]))
        
        except Exception as erro:
            messagebox.showerror("Erro", f"Erro ao listar usuários: {erro}")
        finally:
            conexao.close()

def limpa_campos(entry_nome_usuario, entry_senha_usuario):
    entry_nome_usuario.delete(0, tk.END)
    entry_senha_usuario.delete(0, tk.END)            

def adicionar_usuario(entry_nome_usuario, entry_senha_usuario, treeview):
    nome_usuario = entry_nome_usuario.get()
    senha_usuario = entry_senha_usuario.get()

    if not nome_usuario or not senha_usuario:
        messagebox.showwarning("Atenção", "Preencha todos os campos para adicionar o usuário.")
        return

    senha_hash = bcrypt.hashpw(senha_usuario.encode('utf-8'), bcrypt.gensalt())

    conexao = conectar()
    if conexao:
        try:
            cursor = conexao.cursor()
            cursor.execute("INSERT INTO usuarios (usuario, senha) VALUES (%s, %s)", (nome_usuario, senha_hash))
            conexao.commit()
            messagebox.showinfo("Sucesso", "Usuário adicionado com sucesso!")
            listar_usuarios(treeview) 
            limpa_campos(entry_nome_usuario, entry_senha_usuario) 
        except Exception as erro:
            messagebox.showerror("Erro", f"Erro ao adicionar usuário: {erro}")
        finally:
            conexao.close()

def excluir_usuario(treeview):
    selected_item = treeview.selection()

    if not selected_item:
        messagebox.showwarning("Atenção", "Selecione um usuário para excluir.")
        return

    usuario_id = treeview.item(selected_item)["values"][0]

    conexao = conectar()
    if conexao:
        try:
            cursor = conexao.cursor()
            cursor.execute("DELETE FROM usuarios WHERE id = %s", (usuario_id,))
            conexao.commit()
            messagebox.showinfo("Sucesso", "Usuário excluído com sucesso!")
            listar_usuarios(treeview)
        except Exception as erro:
            messagebox.showerror("Erro", f"Erro ao excluir usuário: {erro}")
        finally:
            conexao.close()

def editar_usuario(entry_nome_usuario, entry_senha_usuario, treeview):
    selected_item = treeview.selection()

    if not selected_item:
        messagebox.showwarning("Atenção", "Selecione um usuário para editar.")
        return

    usuario_id = treeview.item(selected_item)["values"][0]
    nome_usuario = entry_nome_usuario.get()
    senha_usuario = entry_senha_usuario.get()

    if not nome_usuario or not senha_usuario:
        messagebox.showwarning("Atenção", "Preencha todos os campos para editar o usuário.")
        return

    senha_hash = bcrypt.hashpw(senha_usuario.encode('utf-8'), bcrypt.gensalt())

    conexao = conectar()
    if conexao:
        try:
            cursor = conexao.cursor()
            cursor.execute("UPDATE usuarios SET usuario = %s, senha = %s WHERE id = %s", 
                           (nome_usuario, senha_hash, usuario_id))
            conexao.commit()
            messagebox.showinfo("Sucesso", "Usuário atualizado com sucesso!")
            listar_usuarios(treeview)
            limpa_campos(entry_nome_usuario, entry_senha_usuario) 
        except Exception as erro:
            messagebox.showerror("Erro", f"Erro ao editar usuário: {erro}")
        finally:
            conexao.close()

def janela_principal():
    # Janela Principal
    janela_usuarios = tk.Tk()
    janela_usuarios.title("Gerenciamento de Usuários")
    janela_usuarios.geometry("600x400")
    janela_usuarios.resizable(False, False)

    # Frame de Cadastro de Usuário
    frame_cadastro = tk.Frame(janela_usuarios)
    frame_cadastro.pack(pady=20)

    tk.Label(frame_cadastro, text="Nome de Usuário:").grid(row=0, column=0, padx=10)
    entry_nome_usuario = tk.Entry(frame_cadastro)
    entry_nome_usuario.grid(row=0, column=1, padx=10)

    tk.Label(frame_cadastro, text="Senha:").grid(row=1, column=0, padx=10)
    entry_senha_usuario = tk.Entry(frame_cadastro, show="*")
    entry_senha_usuario.grid(row=1, column=1, padx=10)

    # Botões
    tk.Button(frame_cadastro, text="Adicionar Usuário", command=lambda: adicionar_usuario(entry_nome_usuario, entry_senha_usuario, treeview)).grid(row=2, column=0, padx=10, pady=10)
    tk.Button(frame_cadastro, text="Editar Usuário", command=lambda: editar_usuario(entry_nome_usuario, entry_senha_usuario, treeview)).grid(row=2, column=1, padx=10)
    tk.Button(frame_cadastro, text="Excluir Usuário", command=lambda: excluir_usuario(treeview)).grid(row=2, column=2, padx=10)

    # Lista de Usuários (usando ttk.Treeview)
    treeview = ttk.Treeview(janela_usuarios, columns=("ID", "Usuário"), show="headings")
    treeview.heading("ID", text="ID")
    treeview.heading("Usuário", text="Usuário")
    treeview.pack(pady=20)

    # Atualiza a lista de usuários
    listar_usuarios(treeview)

    # Iniciar a janela
    janela_usuarios.mainloop()
