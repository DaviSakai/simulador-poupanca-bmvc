// =========================
//  Formatação BR
// =========================
function formatarMoeda(valor) {
  if (isNaN(valor)) return "R$ 0,00";

  return valor.toLocaleString("pt-BR", {
      style: "currency",
      currency: "BRL",
      minimumFractionDigits: 2
  });
}

// =========================
//  Seleção dos campos
// =========================
const campoValor = document.getElementById("valor_mensal");
const campoMeses = document.getElementById("qt_meses");
const campoJuros = document.getElementById("taxa_juros");
const campoCategoria = document.getElementById("categoria");

const prevInvest = document.getElementById("p_invest");
const prevJuros = document.getElementById("p_juros");
const prevTotal = document.getElementById("p_total");

// =========================
//  Normalizar vírgulas -> ponto
// =========================
function limparNumeroBR(valor) {
  if (!valor) return 0;
  return Number(valor.replace(",", "."));
}

// =========================
//  Atualizar categoria automaticamente
// =========================
function atualizarCategoria() {
  const meses = limparNumeroBR(campoMeses.value);

  if (!meses || meses <= 0) return;

  if (meses <= 12) campoCategoria.value = "curto";
  else if (meses <= 60) campoCategoria.value = "medio";
  else campoCategoria.value = "longo";
}

// =========================
//  Cálculo da estimativa rápida
// =========================
function atualizarPreview() {
  const valor = limparNumeroBR(campoValor.value);
  const meses = limparNumeroBR(campoMeses.value);
  const jurosAnual = limparNumeroBR(campoJuros.value) / 100;

  if (!valor || !meses) {
      prevInvest.textContent = "Você investirá: R$ 0";
      prevJuros.textContent = "Com juros estimados: R$ 0";
      prevTotal.innerHTML = "<strong>Total final estimado: R$ 0</strong>";
      return;
  }

  const totalInvestido = valor * meses;
  let totalFinal = totalInvestido;

  if (jurosAnual > 0) {
      const jurosMensal = (1 + jurosAnual) ** (1 / 12) - 1;

      for (let i = 0; i < meses; i++) {
          totalFinal += valor * jurosMensal * (meses - i);
      }
  }

  const jurosGanhos = totalFinal - totalInvestido;

  prevInvest.textContent = "Você investirá: " + formatarMoeda(totalInvestido);
  prevJuros.textContent = "Com juros estimados: " + formatarMoeda(jurosGanhos);
  prevTotal.innerHTML = "<strong>Total final estimado: " + formatarMoeda(totalFinal) + "</strong>";
}

// =========================
//  Eventos (corrigidos)
// =========================
document.addEventListener("DOMContentLoaded", () => {
  if (campoValor) campoValor.addEventListener("input", atualizarPreview);
  if (campoMeses) campoMeses.addEventListener("input", () => {
      atualizarCategoria();
      atualizarPreview();
  });
  if (campoJuros) campoJuros.addEventListener("input", atualizarPreview);

  atualizarCategoria();
  atualizarPreview();
});
