# 🛠️ APEX - Sistema de Gerenciamento com Interface Gráfica e Banco de Dados

Bem-vindo ao repositório de nossa **APEX**, aonde desenvolvemos um sistema de gerenciamento de cadastros e operações administrativas com interface gráfica em Python, integração com banco de dados MySQL e geração automatizada de documentos de ordem de serviço.

---

## 🚀 Funcionalidades

- 🧑‍💼 Cadastro e edição de **clientes**, **cidades**, **produtos** e **usuários**
- 🧾 Geração e edição de **ordens de serviço (OS)**
- 📄 Substituição automática de dados em documentos `.doc` com marcadores `@`
- 🔒 Sistema de **login com controle de acesso**
- 🔍 Grid de consultas com **seleção clicável**
- 🖨️ Impressão de relatórios e visualização de ordens de serviço

---

## 🧰 Tecnologias Utilizadas

- **Python 3**
- **Tkinter** (Interface gráfica)
- **MySQL Connector**
- **ConfigParser**
- **python-docx** (substituição de texto em .doc)
- **MySQL** (Banco de dados relacional)

---

## 🗂️ Estrutura do Projeto

├── clientes.py
├── cidades.py
├── produtos.py
├── usuarios.py
├── ordem_servico.py
├── editar_cliente.py
├── editar_produto.py
├── os_editar.py
├── os_dados.py
├── os_produtos.py
├── os_servicos.py
├── impressao_osv.py
├── conexao.py
├── bd.ini
├── login.py
└── main.py

---

## ⚙️ Como Executar

# 1. Clone o repositório
git clone https://github.com/GianMarcosBoaretto/APEX_BANCO_DE_DADOS.git
cd APEX_BANCO_DE_DADOS

# 2. Instale as dependências
pip install mysql-connector-python python-docx

# 3. Configure o arquivo bd.ini (edite com seu editor preferido)
echo "[mysql]
host = localhost
user = SEU_USUARIO
password = SUA_SENHA
database = NOME_DO_BANCO" > bd.ini

# 4. Execute o sistema
py -m PyInstaller --onefile --noconsole --icon=icon.ico --name=apex_software login.py

---

## ⚙️ Acessos Iniciais

**Usuário inicial será "admin" e senha "123".**
**Caso deseje alterar, pressione "F12", digite a senha do "admin" e você terá acesso ao gerenciamento de usuários.**




