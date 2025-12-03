from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware

from models import (
    MetaPoupancaRepository,
    autenticar_usuario,
    buscar_usuario,
    criar_usuario
)

# ============================================================
# 🔵 1. CONFIGURAÇÃO PRINCIPAL DO APP
# ============================================================

app = FastAPI()

# Sessão para login persistente
app.add_middleware(SessionMiddleware, secret_key="chave-super-secreta-123")

# Diretórios
BASE_DIR = Path(__file__).resolve().parent

# Static (CSS, JS)
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")

# Repositório de metas
meta_repo = MetaPoupancaRepository()


# ============================================================
# 🔵 2. FUNÇÕES AUXILIARES DE AUTENTICAÇÃO
# ============================================================

def usuario_logado(request: Request):
    """Retorna o usuário logado (ou None)."""
    return request.session.get("user")


def proteger(request: Request):
    """Redireciona para /login caso o usuário não esteja autenticado."""
    if not usuario_logado(request):
        return RedirectResponse(url="/login", status_code=303)


# ============================================================
# 🔵 3. ROTAS PÚBLICAS (Simulador + Login + Cadastro)
# ============================================================

# --- PÁGINA INICIAL (Simulador livre) ---
@app.get("/", response_class=HTMLResponse)
def abrir_simulador():
    html_path = BASE_DIR / "view" / "simulador.html"
    try:
        return html_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return HTMLResponse(
            content=f"<h2>Erro: simulador não encontrado em {html_path}</h2>",
            status_code=500
        )


# =============================
# 🔐 LOGIN
# =============================
@app.get("/login")
async def login_get(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.post("/login")
async def login_post(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
):
    usuario = autenticar_usuario(username, password)

    if not usuario:
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "erro": "Usuário ou senha inválidos."},
            status_code=401
        )

    # Salva usuário na sessão
    request.session["user"] = usuario.model_dump()

    return RedirectResponse(url="/restrito", status_code=303)


@app.get("/logout")
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/login", status_code=303)


# =============================
# 🟦 CADASTRO
# =============================
@app.get("/cadastro")
async def cadastro_get(request: Request):
    return templates.TemplateResponse("cadastro.html", {"request": request})


@app.post("/cadastro")
async def cadastro_post(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
):

    # Verifica se o usuário já existe
    if buscar_usuario(username):
        return templates.TemplateResponse(
            "cadastro.html",
            {"request": request, "erro": "Usuário já existe."}
        )

    # Cria e salva o usuário
    criar_usuario(username, password)

    return RedirectResponse(url="/login", status_code=303)


# ============================================================
# 🔵 4. ÁREA RESTRITA (Dashboard protegido)
# ============================================================

@app.get("/restrito")
async def restrito(request: Request):
    if proteger(request):
        return proteger(request)

    user = usuario_logado(request)

    return templates.TemplateResponse(
        "restrito.html",
        {"request": request, "usuario": user}
    )


# ============================================================
# 🔵 5. CRUD DE METAS (totalmente protegido)
# ============================================================

# --- LISTAR METAS ---
@app.get("/metas", response_class=HTMLResponse)
def listar_metas(request: Request):
    if proteger(request):
        return proteger(request)

    metas = meta_repo.listar()
    return templates.TemplateResponse(
        "metas/listar.html",
        {"request": request, "metas": metas, "usuario": usuario_logado(request)}
    )


# --- FORM NOVA META ---
@app.get("/metas/nova", response_class=HTMLResponse)
def form_nova_meta(request: Request):
    if proteger(request):
        return proteger(request)

    return templates.TemplateResponse(
        "metas/form.html",
        {"request": request, "meta": None, "acao": "criar", "usuario": usuario_logado(request)}
    )


# --- CRIAR META ---
@app.post("/metas/criar")
def criar_meta(
    request: Request,
    nome: str = Form(...),
    categoria: str = Form(...),
    valor_mensal: float = Form(...),
    qt_meses: int = Form(...),
    taxa_juros: float = Form(...),
):
    if proteger(request):
        return proteger(request)

    meta_repo.criar(nome, categoria, valor_mensal, qt_meses, taxa_juros)
    return RedirectResponse(url="/metas", status_code=303)


# --- EDITAR META ---
@app.get("/metas/{meta_id}/editar", response_class=HTMLResponse)
def form_editar_meta(meta_id: int, request: Request):
    if proteger(request):
        return proteger(request)

    meta = meta_repo.buscar_por_id(meta_id)
    if not meta:
        return RedirectResponse(url="/metas", status_code=303)

    return templates.TemplateResponse(
        "metas/form.html",
        {"request": request, "meta": meta, "acao": "editar", "usuario": usuario_logado(request)}
    )


# --- ATUALIZAR META ---
@app.post("/metas/{meta_id}/atualizar")
def atualizar_meta(
    meta_id: int,
    request: Request,
    nome: str = Form(...),
    categoria: str = Form(...),
    valor_mensal: float = Form(...),
    qt_meses: int = Form(...),
    taxa_juros: float = Form(...),
):
    if proteger(request):
        return proteger(request)

    meta_repo.atualizar(meta_id, nome, categoria, valor_mensal, qt_meses, taxa_juros)
    return RedirectResponse(url="/metas", status_code=303)


# --- EXCLUIR META ---
@app.post("/metas/{meta_id}/excluir")
def excluir_meta(meta_id: int, request: Request):
    if proteger(request):
        return proteger(request)

    meta_repo.excluir(meta_id)
    return RedirectResponse(url="/metas", status_code=303)
