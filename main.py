from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path

app = FastAPI()

# Caminho base do projeto
BASE_DIR = Path(__file__).resolve().parent

# Monta a pasta "static" para CSS e JS
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")

# Rota principal — exibe o simulador
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
