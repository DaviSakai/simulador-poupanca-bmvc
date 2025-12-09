# 💰 Simulador de Poupança Mensal — BMVC 

Projeto desenvolvido por **Davi Sakai** para o módulo **BMVC** de Orientação a Objetos,  
com o objetivo de tornar a **educação financeira acessível,moderna e intuitiva**.

---

## 🎯 Objetivo do Projeto

O **Planejador de Metas Financeiras** permite que o usuário:

- Crie e gerencie metas financeiras 🎯
- Simule crescimento com aportes mensais 🧮
- Visualize o impacto dos juros compostos 📈
- Organize sua vida financeira de forma profissional e prática 🧠

Além disso, conta com um sistema seguro de login, área restrita e interface inspirada em grandes plataformas financeiras.

O sistema inclui:

- Login, cadastro e sessão persistente 🔐

- CRUD completo de metas financeiras 🗂️

- Persistência em arquivos JSON 📦

- Interface moderna inspirada em plataformas reais 🎨
---

## 🧱 Estrutura do Projeto

```bash
simulador-poupanca-bmvc/
│
├── main.py                      → Servidor FastAPI + rotas + autenticação
├── models.py                    → Persistência em JSON (usuários + metas)
│
├── controller/                  → Controladores (MVC)
│   └── simulador_controller.py  → Controller do simulador público
│
├── model/                       → Modelos (lógica de negócio)
│   └── simulador_model.py       → Cálculos de poupança
│
├── metas.json                   → Banco de dados de metas
├── usuarios.json                → Banco de dados de usuários
│
├── templates/                   → Páginas HTML (Jinja2)
│   ├── base.html                
│   ├── login.html               
│   ├── cadastro.html            
│   ├── restrito.html            
│   └── metas/
│       ├── listar.html          
│       └── form.html            
│
├── static/
│   ├── css/
│   │   ├── core.css             
│   │   ├── auth.css             
│   │   └── metas.css            
│   └── js/
│       └── simulador.js         
│
└── view/
    └── simulador.html           → Simulador público (sem login)

```

## 🧠 Arquitetura BMVC
```bash

# Model

- model/simulador_model.py → cálculos matemáticos (juros compostos)
- models.py → repositórios e persistência JSON
- Totalmente isolado, sem lógica de controller ou view

# View

- HTML, CSS e JS
- Templates Jinja2
- Interface limpa e responsiva
- Sem lógica de negócio

# Controller

- controller/simulador_controller.py
- Recebe requisições, chama o Model e envia resposta à View
- Mantém o encapsulamento e separação de camadas

# Main

- Ponto de entrada do sistema
- Registra controllers
- Gerencia sessão, autenticação e rotas
- Não possui lógica de negócio


```
## 📌 Funcionalidades
```bash


# Área Pública

- Simulador de poupança
- Processamento dinâmico via JavaScript
- Cálculo com e sem juros compostos

# Área Privada

- Login, cadastro e logout
- Sessão persistente
- Dashboard do usuário
- CRUD completo de metas financeiras

# Técnicas Utilizadas

- FastAPI
- Jinja2 Templates
- Repository Pattern
- Arquitetura BMVC
- Persistência JSON
- Encapsulamento e separação de responsabilidades
```

## ⚙️ Como Executar o Projeto

```bash
# 1️⃣ Clone o repositório
git clone https://github.com/DaviSakai/simulador-poupanca-bmvc.git
cd simulador-poupanca-bmvc

# 2️⃣ Crie o ambiente virtual (Windows)
python -m venv .venv
.venv\Scripts\activate

# 3️⃣ Instale as dependências
pip install fastapi uvicorn

# 4️⃣ Execute o servidor
uvicorn main:app --reload

# 5️⃣ Acesse no navegador
http://127.0.0.1:8000/
