import json
from pathlib import Path
from pydantic import BaseModel

# ============================================================
# 🔵 CONFIGURAÇÃO DE ARQUIVO (Usuários)
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
USERS_FILE = BASE_DIR / "usuarios.json"

if not USERS_FILE.exists():
    USERS_FILE.write_text("[]", encoding="utf-8")


# ============================================================
# 🔵 MODELO Pydantic para Usuário
# ============================================================

class Usuario(BaseModel):
    username: str
    password: str   # (simples; depois podemos colocar hash)


# ============================================================
# 🔵 FUNÇÕES DE USUÁRIOS
# ============================================================

def carregar_usuarios():
    """Lê todos os usuários do arquivo JSON."""
    try:
        return json.loads(USERS_FILE.read_text(encoding="utf-8"))
    except:
        return []


def salvar_usuarios(lista):
    """Salva lista completa de usuários no JSON."""
    USERS_FILE.write_text(
        json.dumps(lista, indent=4, ensure_ascii=False),
        encoding="utf-8"
    )


def buscar_usuario(username: str):
    """Retorna o dicionário do usuário se existir."""
    usuarios = carregar_usuarios()
    for u in usuarios:
        if u["username"] == username:
            return u
    return None


def criar_usuario(username: str, password: str):
    """Cria e salva um novo usuário."""
    usuarios = carregar_usuarios()

    novo = Usuario(username=username, password=password)
    usuarios.append(novo.model_dump())

    salvar_usuarios(usuarios)
    return novo


def autenticar_usuario(username: str, password: str):
    """Retorna o usuário se login for válido, senão None."""
    usuario = buscar_usuario(username)

    if usuario and usuario["password"] == password:
        return Usuario(**usuario)  # retorna modelo Pydantic
    return None



# ============================================================
# 🔵 FUNÇÕES DAS METAS 
# ============================================================

class MetaPoupancaRepository:
    def __init__(self):
        self.arquivo = BASE_DIR / "metas.json"
        if not self.arquivo.exists():
            self.arquivo.write_text("[]", encoding="utf-8")

    def listar(self):
        return json.loads(self.arquivo.read_text(encoding="utf-8"))

    def salvar(self, lista):
        self.arquivo.write_text(json.dumps(lista, indent=4), encoding="utf-8")

    def criar(self, nome, categoria, valor_mensal, qt_meses, taxa_juros):
        metas = self.listar()
        novo_id = 1 if not metas else metas[-1]["id"] + 1

        meta = {
            "id": novo_id,
            "nome": nome,
            "categoria": categoria,
            "valor_mensal": valor_mensal,
            "qt_meses": qt_meses,
            "taxa_juros": taxa_juros
        }

        metas.append(meta)
        self.salvar(metas)
        return meta

    def buscar_por_id(self, meta_id):
        metas = self.listar()
        for m in metas:
            if m["id"] == meta_id:
                return m
        return None

    def atualizar(self, meta_id, nome, categoria, valor_mensal, qt_meses, taxa_juros):
        metas = self.listar()
        for m in metas:
            if m["id"] == meta_id:
                m.update({
                    "nome": nome,
                    "categoria": categoria,
                    "valor_mensal": valor_mensal,
                    "qt_meses": qt_meses,
                    "taxa_juros": taxa_juros
                })
                break
        self.salvar(metas)

    def excluir(self, meta_id):
        metas = self.listar()
        metas = [m for m in metas if m["id"] != meta_id]
        self.salvar(metas)
