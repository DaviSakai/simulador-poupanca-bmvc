# 💰 Simulador de Poupança Mensal — BMVC I

Projeto desenvolvido por **Davi Sakai** para o módulo **BMVC** de Orientação a Objetos,  
com o objetivo de tornar a **educação financeira acessível** e intuitiva.

---

## 🎯 Objetivo do Projeto

O **Simulador de Poupança Mensal** permite visualizar, de forma simples e didática,  
quanto o dinheiro pode crescer com **depósitos mensais** — com e sem rendimento.  

Ele foi feito para ajudar **iniciantes em investimentos** a compreenderem conceitos como:
- Acúmulo de capital com constância 💡  
- Juros compostos e rendimento percentual 📈  
- Diferença entre guardar e investir com rentabilidade 🧠  

---

## 🧱 Estrutura do Projeto

```bash
simulador-poupanca-bmvc/
│
├── main.py              → servidor FastAPI que serve o app
│
├── view/
│   └── simulador.html    → interface principal do simulador
│
└── static/
    ├── css/
    │   └── simulador.css → estilo visual moderno e responsivo
    └── js/
        └── simulador.js  → lógica da simulação (juros e cálculos)
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
