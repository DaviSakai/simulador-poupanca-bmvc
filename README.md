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

---

## 🧱 Estrutura do Projeto

```bash
simulador-poupanca-bmvc/
│
├── main.py                      → servidor FastAPI + rotas + autenticação
├── models.py                    → persistência em JSON (metas e usuários)
│
├── templates/                   → páginas HTML com Jinja2
│   ├── base.html                → layout principal
│   ├── login.html               → página de login moderna
│   ├── cadastro.html            → criação de conta
│   ├── restrito.html            → dashboard do usuário
│   └── metas/
│       ├── listar.html          → listagem de metas
│       └── form.html            → criar/editar metas
│
├── static/
│   ├── css/
│   │   ├── core.css             → estilo global
│   │   ├── auth.css             → login/cadastro
│   │   └── metas.css            → página de metas
│   └── js/
│       └── simulador.js         → cálculos do simulador
│
└── view/
    └── simulador.html           → simulador público (sem login)

```


---

## 🖥️ Inspiração

```bash
A interface foi inspirada em simuladores de grandes portais como **iDinheiro**, **Serasa** e **BTG Pactual**,  
mantendo uma identidade leve, educativa e profissional.

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
