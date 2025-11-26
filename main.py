from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from fastapi.templating import Jinja2Templates
from models import MetaPoupancaRepository
from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse

app = FastAPI()

# Caminho base do projeto
BASE_DIR = Path(__file__).resolve().parent

# Monta a pasta "static" para CSS e JS
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")

# ---------------- ROTA PRINCIPAL ----------------
@app.get("/", response_class=HTMLResponse)
def abrir_simulador():
    html_path = BASE_DIR / "view" / "simulador.html"
    try:
        return html_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return HTMLResponse(
            content=f"<h2>Erro: arquivo não encontrado em {html_path}</h2>",
            status_code=500
        )

# ---------------- CONFIG TEMPLATES ----------------
templates = Jinja2Templates(directory="templates")

# ---------------- REPOSITÓRIO ----------------
meta_repo = MetaPoupancaRepository()

# =============== ROTAS CRUD METAS ===============

@app.get("/metas", response_class=HTMLResponse)
def listar_metas(request: Request):
    metas = meta_repo.listar()
    return templates.TemplateResponse(
        "metas/listar.html",
        {"request": request, "metas": metas}
    )


@app.get("/metas/nova", response_class=HTMLResponse)
def form_nova_meta(request: Request):
    return templates.TemplateResponse(
        "metas/form.html",
        {"request": request, "meta": None, "acao": "criar"}
    )


@app.post("/metas/criar")
def criar_meta(
    nome: str = Form(...),
    categoria: str = Form(...),              
    valor_mensal: float = Form(...),
    qt_meses: int = Form(...),
    taxa_juros: float = Form(...)
):
    meta_repo.criar(nome, categoria, valor_mensal, qt_meses, taxa_juros)
    return RedirectResponse(url="/metas", status_code=303)


@app.get("/metas/{meta_id}/editar", response_class=HTMLResponse)
def form_editar_meta(meta_id: int, request: Request):
    meta = meta_repo.buscar_por_id(meta_id)
    if not meta:
        return RedirectResponse(url="/metas", status_code=303)

    return templates.TemplateResponse(
        "metas/form.html",
        {"request": request, "meta": meta, "acao": "editar"}
    )


@app.post("/metas/{meta_id}/atualizar")
def atualizar_meta(
    meta_id: int,
    nome: str = Form(...),
    categoria: str = Form(...),            
    valor_mensal: float = Form(...),
    qt_meses: int = Form(...),
    taxa_juros: float = Form(...)
):
    meta_repo.atualizar(meta_id, nome, categoria, valor_mensal, qt_meses, taxa_juros)
    return RedirectResponse(url="/metas", status_code=303)


@app.post("/metas/{meta_id}/excluir")
def excluir_meta(meta_id: int):
    meta_repo.excluir(meta_id)
    return RedirectResponse(url="/metas", status_code=303)
