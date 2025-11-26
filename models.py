import json
import os

ARQUIVO_METAS = "metas.json"


# ===========================
#   MODELO DE DADOS
# ===========================
class MetaPoupanca:
    def __init__(self, id, nome, categoria, valor_mensal, qt_meses, taxa_juros):
        self.id = id
        self.nome = nome
        self.categoria = categoria          # <-- NOVO CAMPO
        self.valor_mensal = valor_mensal
        self.qt_meses = qt_meses
        self.taxa_juros = taxa_juros

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "categoria": self.categoria,
            "valor_mensal": self.valor_mensal,
            "qt_meses": self.qt_meses,
            "taxa_juros": self.taxa_juros
        }


# ===========================
#   REPOSITÓRIO
# ===========================
class MetaPoupancaRepository:
    def __init__(self):
        if not os.path.exists(ARQUIVO_METAS):
            with open(ARQUIVO_METAS, "w", encoding="utf-8") as f:
                json.dump([], f, ensure_ascii=False, indent=4)

    # Carregar todas metas
    def _carregar(self):
        with open(ARQUIVO_METAS, "r", encoding="utf-8") as f:
            return json.load(f)

    # Salvar lista completa
    def _salvar(self, lista):
        with open(ARQUIVO_METAS, "w", encoding="utf-8") as f:
            json.dump(lista, f, ensure_ascii=False, indent=4)

    # ===========================
    #   CRUD
    # ===========================

    def listar(self):
        dados = self._carregar()
        return [MetaPoupanca(**d) for d in dados]

    def buscar_por_id(self, meta_id: int):
        dados = self._carregar()
        for d in dados:
            if d["id"] == meta_id:
                return MetaPoupanca(**d)
        return None

    def criar(self, nome, categoria, valor_mensal, qt_meses, taxa_juros):
        dados = self._carregar()

        novo_id = 1 if not dados else dados[-1]["id"] + 1

        nova_meta = MetaPoupanca(
            id=novo_id,
            nome=nome,
            categoria=categoria,
            valor_mensal=valor_mensal,
            qt_meses=qt_meses,
            taxa_juros=taxa_juros
        )

        dados.append(nova_meta.to_dict())
        self._salvar(dados)

    def atualizar(self, meta_id, nome, categoria, valor_mensal, qt_meses, taxa_juros):
        dados = self._carregar()

        for d in dados:
            if d["id"] == meta_id:
                d["nome"] = nome
                d["categoria"] = categoria
                d["valor_mensal"] = valor_mensal
                d["qt_meses"] = qt_meses
                d["taxa_juros"] = taxa_juros
                break

        self._salvar(dados)

    def excluir(self, meta_id):
        dados = self._carregar()
        dados = [d for d in dados if d["id"] != meta_id]
        self._salvar(dados)
