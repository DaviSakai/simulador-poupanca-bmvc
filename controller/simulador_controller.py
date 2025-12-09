from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from pathlib import Path
from model.simulador_model import calcular_simulacao

router = APIRouter()

# Caminho base do projeto
BASE_DIR = Path(__file__).resolve().parents[1]


# 📌 Página inicial do simulador (página pública)
@router.get("/", response_class=HTMLResponse)
async def abrir_simulador():
    simulador_path = BASE_DIR / "view" / "simulador.html"

    try:
        return simulador_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return HTMLResponse(
            f"<h2>Erro: arquivo não encontrado em {simulador_path}</h2>",
            status_code=500
        )


# 📌 API de processamento — retorna JSON para o JavaScript do simulador
@router.post("/simular")
async def simular(
    valorMensal: float = Form(...),
    qtMeses: int = Form(...),
    taxaMensal: float = Form(0.0)
):
    resultado = calcular_simulacao(valorMensal, qtMeses, taxaMensal)

    return {
        "totalSemJuros": resultado["total_sem_juros"],
        "totalComJuros": resultado["total_com_juros"],
        "diferenca": resultado["diferenca"]
    }
