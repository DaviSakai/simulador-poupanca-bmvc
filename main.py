from pathlib import Path
from typing import List

from fastapi import FastAPI, Request, Form, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware

# Controllers
from controller.simulador_controller import router as simulador_router

# Models / Repositórios
from models import (
    MetaPoupancaRepository,
    autenticar_usuario,
    buscar_usuario,
    criar_usuario,
)

# ============================================================
# 1. CONFIGURAÇÃO PRINCIPAL DO APP
# ============================================================

app = FastAPI()

app.add_middleware(SessionMiddleware, secret_key="chave-super-secreta-123")

BASE_DIR = Path(__file__).resolve().parent

# Static (CSS, JS)
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")

# Repositório de metas
meta_repo = MetaPoupancaRepository()

# Controller do simulador (rota "/")
app.include_router(simulador_router)

# ============================================================
# 2. FUNÇÕES AUXILIARES DE AUTENTICAÇÃO
# ============================================================

def usuario_logado(request: Request):
    return request.session.get("user")


def proteger(request: Request):
    """
    Se não houver usuário logado, devolve um RedirectResponse para /login.
    Se houver usuário, devolve None.
    """
    if not usuario_logado(request):
        return RedirectResponse(url="/login", status_code=303)
    return None


# ============================================================
# 3. LOGIN / CADASTRO
# ============================================================

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
            status_code=401,
        )

    # Salva usuário (dict) na sessão
    request.session["user"] = usuario.model_dump()
    return RedirectResponse(url="/restrito", status_code=303)


@app.get("/logout")
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/login", status_code=303)


@app.get("/cadastro")
async def cadastro_get(request: Request):
    return templates.TemplateResponse("cadastro.html", {"request": request})


@app.post("/cadastro")
async def cadastro_post(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
):
    if buscar_usuario(username):
        return templates.TemplateResponse(
            "cadastro.html",
            {"request": request, "erro": "Usuário já existe."},
        )

    criar_usuario(username, password)
    return RedirectResponse(url="/login", status_code=303)


# ============================================================
# 4. ÁREA RESTRITA
# ============================================================

@app.get("/restrito")
async def restrito(request: Request):
    protecao = proteger(request)
    if protecao:
        return protecao

    user = usuario_logado(request)
    return templates.TemplateResponse(
        "restrito.html",
        {"request": request, "usuario": user},
    )


# ============================================================
# 5. GERENCIADOR DE WEBSOCKET PARA METAS
# ============================================================

class MetasWebSocketManager:
    """
    Mantém as conexões WebSocket ativas e envia atualizações
    sempre que as metas forem alteradas (criar / editar / excluir).
    """

    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def send_snapshot(self, websocket: WebSocket):
        """
        Envia o estado atual das metas apenas para um websocket específico.
        """
        metas = meta_repo.listar()
        await websocket.send_json(
            {
                "type": "metas_update",
                "metas": metas,
            }
        )

    async def broadcast_metas(self):
        """
        Envia a lista completa de metas para TODAS as conexões ativas.
        Chamado após criar / atualizar / excluir.
        """
        if not self.active_connections:
            return

        metas = meta_repo.listar()
        payload = {
            "type": "metas_update",
            "metas": metas,
        }

        # Envia para todos; remove quem caiu
        for websocket in list(self.active_connections):
            try:
                await websocket.send_json(payload)
            except Exception:
                # se der erro (inclusive WebSocketDisconnect),
                # removemos a conexão da lista
                self.disconnect(websocket)


metas_ws_manager = MetasWebSocketManager()


@app.websocket("/ws/metas")
async def metas_websocket(websocket: WebSocket):
    """
    Endpoint WebSocket para acompanhar as metas em tempo real.
    A página /metas.js se conecta aqui.
    """
    await metas_ws_manager.connect(websocket)

    try:
        # Ao conectar, já manda o snapshot inicial
        await metas_ws_manager.send_snapshot(websocket)

        # Mantém conexão "viva".
        # Podemos receber mensagens do cliente se quisermos (ex: ping),
        # mas aqui só lemos e ignoramos.
        while True:
            await websocket.receive_text()

    except WebSocketDisconnect:
        metas_ws_manager.disconnect(websocket)
    except Exception:
        metas_ws_manager.disconnect(websocket)


# ============================================================
# 6. CRUD DE METAS (AGORA ASSÍNCRONO + BROADCAST)
# ============================================================

@app.get("/metas", response_class=HTMLResponse)
async def listar_metas(request: Request):
    protecao = proteger(request)
    if protecao:
        return protecao

    metas = meta_repo.listar()

    return templates.TemplateResponse(
        "metas/listar.html",
        {
            "request": request,
            "metas": metas,
            "usuario": usuario_logado(request),
        },
    )


@app.get("/metas/nova", response_class=HTMLResponse)
async def form_nova_meta(request: Request):
    protecao = proteger(request)
    if protecao:
        return protecao

    return templates.TemplateResponse(
        "metas/form.html",
        {
            "request": request,
            "meta": None,
            "acao": "criar",
            "usuario": usuario_logado(request),
        },
    )


@app.post("/metas/criar")
async def criar_meta(
    request: Request,
    nome: str = Form(...),
    categoria: str = Form(...),
    valor_mensal: float = Form(...),
    qt_meses: int = Form(...),
    taxa_juros: float = Form(...),
):
    protecao = proteger(request)
    if protecao:
        return protecao

    meta_repo.criar(nome, categoria, valor_mensal, qt_meses, taxa_juros)

    # Notifica todos os WebSockets
    await metas_ws_manager.broadcast_metas()

    return RedirectResponse(url="/metas", status_code=303)


@app.get("/metas/{meta_id}/editar", response_class=HTMLResponse)
async def form_editar_meta(meta_id: int, request: Request):
    protecao = proteger(request)
    if protecao:
        return protecao

    meta = meta_repo.buscar_por_id(meta_id)
    if not meta:
        return RedirectResponse(url="/metas", status_code=303)

    return templates.TemplateResponse(
        "metas/form.html",
        {
            "request": request,
            "meta": meta,
            "acao": "editar",
            "usuario": usuario_logado(request),
        },
    )


@app.post("/metas/{meta_id}/atualizar")
async def atualizar_meta(
    meta_id: int,
    request: Request,
    nome: str = Form(...),
    categoria: str = Form(...),
    valor_mensal: float = Form(...),
    qt_meses: int = Form(...),
    taxa_juros: float = Form(...),
):
    protecao = proteger(request)
    if protecao:
        return protecao

    meta_repo.atualizar(meta_id, nome, categoria, valor_mensal, qt_meses, taxa_juros)

    # Notifica todos os WebSockets
    await metas_ws_manager.broadcast_metas()

    return RedirectResponse(url="/metas", status_code=303)


@app.post("/metas/{meta_id}/excluir")
async def excluir_meta(meta_id: int, request: Request):
    protecao = proteger(request)
    if protecao:
        return protecao

    meta_repo.excluir(meta_id)

    # Notifica todos os WebSockets
    await metas_ws_manager.broadcast_metas()

    return RedirectResponse(url="/metas", status_code=303)
