def calcular_simulacao(valor_mensal: float, meses: int, taxa_mensal: float):
    """
    Calcula o total acumulado com e sem juros compostos.
    """

    total_sem_juros = valor_mensal * meses

    # Caso não exista taxa, não há juros compostos
    if taxa_mensal <= 0:
        return {
            "total_sem_juros": round(total_sem_juros, 2),
            "total_com_juros": round(total_sem_juros, 2),
            "diferenca": 0
        }

    # Converter porcentagem para decimal (ex: 0.6 → 0.006)
    taxa_decimal = taxa_mensal / 100

    total = 0
    for _ in range(meses):
        total = (total + valor_mensal) * (1 + taxa_decimal)

    return {
        "total_sem_juros": round(total_sem_juros, 2),
        "total_com_juros": round(total, 2),
        "diferenca": round(total - total_sem_juros, 2)
    }
