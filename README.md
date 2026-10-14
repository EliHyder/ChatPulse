# 💬 ChatPulse - Sistema de Mensagens Diretas (API & Back-end)

`ChatPulse` é um projeto de back-end desenvolvido em Python utilizando **FastAPI**, **SQLAlchemy** e **SQLite**, focado em gerenciar usuários e um sistema robusto de mensagens diretas (Direct Messages), estruturado com relacionamentos complexos de banco de dados.

---

## 🚀 Tecnologias Utilizadas
* **Python** (Linguagem principal)
* **FastAPI** (Framework web de alta performance)
* **SQLAlchemy** (ORM para gerenciamento e mapeamento do banco de dados relacional)
* **SQLite** (Banco de dados leve e embutido)
* **Pydantic** (Validação de dados e contratos de API)

---

## 📂 Estrutura do Projeto

```text
ChatPulse/
│
├── server/
│   ├── DB/
│   │   ├── db.py           # Conexão com o banco e sessões
│   │   └── models.py       # Definição das tabelas (Users e Messages)
│   ├── routers/
│   │   ├── users.py        # Rotas de gerenciamento de usuários
│   │   └── messages.py     # Rotas de envio e leitura de mensagens
│   ├── schemas.py          # Contratos de validação (Pydantic)
│   └── app.py              # Inicialização do servidor FastAPI
│
├── venv/                   # Ambiente virtual Python
└── README.md               # Documentação do projeto