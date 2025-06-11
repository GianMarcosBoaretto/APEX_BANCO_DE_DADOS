import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import main
from conexao import conectar
import bcrypt
import usuarios



def abrir_user(event):
    # Janela de login secundária (admin)
    janela_login = tk.Tk()
    janela_login.title("Login Admin")
    janela_login.geometry("300x200")
    janela_login.resizable(False, False)

    tk.Label(janela_login, text="Senha do Admin:").pack(pady=5)
    entry_senha2 = tk.Entry(janela_login, show="*")
    entry_senha2.pack()

    def abrir(event=None, entry=None):
        senha_digitada = entry.get()
        conexao = conectar()

        if not conexao:
            messagebox.showerror("Erro", "Não foi possível conectar ao banco de dados.")
            return

        try:
            cursor = conexao.cursor()
            sql = "SELECT senha FROM usuarios WHERE usuario = %s"
            cursor.execute(sql, ("admin",))
            resultado = cursor.fetchone()

            if resultado:
                senha_admin_bd = resultado[0]
                if bcrypt.checkpw(senha_digitada.encode('utf-8'), senha_admin_bd.encode('utf-8')):
                    janela_login.destroy()
                    usuarios.janela_principal()
                else:
                    messagebox.showerror("Erro", "Senha incorreta.")
            else:
                messagebox.showerror("Erro", "Usuário admin não encontrado.")
        except Exception as erro:
            messagebox.showerror("Erro", f"Erro ao verificar senha do admin: {erro}")
        finally:
            conexao.close()

    tk.Button(janela_login, text="Entrar", command=lambda: abrir(None, entry_senha2)).pack(pady=20)
    janela_login.bind("<Return>", lambda event: abrir(event, entry_senha2))


def fazer_login(event=None):
    conexao = conectar()

    if not conexao:
        messagebox.showerror("Erro", "Não foi possível conectar ao banco de dados. Por gentileza, verifique as informações do arquivo bd.ini")
        return

    usuario = entry_usuario.get()
    senha = entry_senha.get()

    try:
        cursor = conexao.cursor()
        sql = "SELECT senha FROM usuarios WHERE usuario = %s"
        cursor.execute(sql, (usuario,))
        resultado = cursor.fetchone()

        if resultado:  # Se o usuário foi encontrado
            senha_bd = resultado[0]
            if bcrypt.checkpw(senha.encode('utf-8'), senha_bd.encode('utf-8')):
                conexao.close()
                janela_login.destroy()
                main.main()
            else:
                messagebox.showerror("Erro", "Usuário ou senha incorretos.")
        else:
            messagebox.showerror("Erro", "Usuário não encontrado.")

    except Exception as erro:
        messagebox.showerror("Erro", f"Erro ao acessar o banco de dados: {erro}")
    finally:
        conexao.close()


# Janela de login principal
janela_login = tk.Tk()
janela_login.title("Login")
janela_login.geometry("300x200")
janela_login.resizable(False, False)

tk.Label(janela_login, text="Usuário:").pack(pady=5)
entry_usuario = tk.Entry(janela_login)
entry_usuario.pack()

tk.Label(janela_login, text="Senha:").pack(pady=5)
entry_senha = tk.Entry(janela_login, show="*")
entry_senha.pack()

tk.Button(janela_login, text="Entrar", command=fazer_login).pack(pady=20)

janela_login.bind("<Return>", fazer_login)
janela_login.bind("<F12>", abrir_user)

janela_login.mainloop()
