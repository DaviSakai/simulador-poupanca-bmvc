// =========================
//  Utilitários de número
// =========================
function formatarMoeda(v) {
  if (isNaN(v)) v = 0;
  return v.toLocaleString("pt-BR", {
    style: "currency",
    currency: "BRL",
  });
}

function toNumber(v) {
  if (v === null || v === undefined) return 0;
  // vem sempre como string do input
  return parseFloat(String(v).replace(",", ".")) || 0;
}

// =========================
//  Lógica principal
// =========================
document.addEventListener("DOMContentLoaded", () => {
  const btnCalcular = document.getElementById("btnCalcular");
  if (!btnCalcular) {
    // se chegar aqui, o botão não existe na página
    return;
  }

  btnCalcular.addEventListener("click", () => {
    const valor = toNumber(document.getElementById("valor_mensal")?.value);
    const meses = toNumber(document.getElementById("qt_meses")?.value);
    const jurosAno = toNumber(document.getElementById("taxa_juros")?.value) / 100;

    const preview = document.getElementById("preview-box");
    const pInvest = document.getElementById("p_invest");
    const pJuros = document.getElementById("p_juros");
    const pTotal = document.getElementById("p_total");

    if (!preview || !pInvest || !pJuros || !pTotal) {
      return; // IDs incorretos → evita erro
    }

    // Caso mínimo: campos obrigatórios não preenchidos
    if (!valor || !meses) {
      preview.style.display = "block";
      pInvest.textContent = "Você investirá: R$ 0";
      pJuros.textContent = "Com juros estimados: R$ 0";
      pTotal.innerHTML = "<b>Total final estimado: R$ 0</b>";
      return;
    }

    const investido = valor * meses;
    let total = investido;

    if (jurosAno > 0) {
      // converte juros anual em mensal efetivo
      const jurosMes = Math.pow(1 + jurosAno, 1 / 12) - 1;
      total = 0;

      // série de aportes mensais com juros compostos
      for (let i = 1; i <= meses; i++) {
        total += valor * Math.pow(1 + jurosMes, meses - i);
      }
    }

    const ganho = total - investido;

    pInvest.textContent = "Você investirá: " + formatarMoeda(investido);
    pJuros.textContent = "Com juros estimados: " + formatarMoeda(ganho);
    pTotal.innerHTML =
      "<b>Total final estimado: " + formatarMoeda(total) + "</b>";

    preview.style.display = "block";
  });
});
