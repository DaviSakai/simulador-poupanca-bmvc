// ======================================================
//               FORMATADOR EM REAL (BRL)
// ======================================================
function formatCurrency(valor) {
  return valor.toLocaleString("pt-BR", {
    style: "currency",
    currency: "BRL",
  });
}

let grafico = null;
let tipoGraficoAtual = "line"; // line | bar | area

// ======================================================
//          LISTENER PRINCIPAL DO FORMULÁRIO
// ======================================================
document.addEventListener("DOMContentLoaded", () => {

  const form = document.getElementById("simulador-form");
  const cardResultado = document.getElementById("resultado");

  const totalSemJurosEl = document.getElementById("totalSemJuros");
  const totalComJurosEl = document.getElementById("totalComJuros");
  const textoDiferencaEl = document.getElementById("textoDiferenca");

  cardResultado.classList.add("result-card--hidden");

  // Botões de troca de gráfico
  document.getElementById("btnLine").onclick = () => trocarTipoGrafico("line");
  document.getElementById("btnBar").onclick = () => trocarTipoGrafico("bar");
  document.getElementById("btnArea").onclick = () => trocarTipoGrafico("area");

  form.addEventListener("submit", (event) => {
    event.preventDefault();

    const valorMensal = parseFloat(document.getElementById("valorMensal").value);
    const qtMeses = parseInt(document.getElementById("qtMeses").value, 10);
    const taxa = parseFloat(
      document.getElementById("taxaMensal").value.replace(",", ".")
    ) || 0;

    // Cálculo sem juros
    const totalSemJuros = valorMensal * qtMeses;

    // Cálculo composto
    let totalComJuros = 0;
    const t = taxa / 100;

    for (let i = 0; i < qtMeses; i++) {
      totalComJuros = (totalComJuros + valorMensal) * (1 + t);
    }

    const diferenca = totalComJuros - totalSemJuros;

    totalSemJurosEl.textContent = formatCurrency(totalSemJuros);
    totalComJurosEl.textContent = formatCurrency(totalComJuros);
    textoDiferencaEl.textContent =
      diferenca > 0
        ? `Você ganhou aproximadamente ${formatCurrency(diferenca)} só em juros.`
        : "";

    cardResultado.classList.remove("result-card--hidden");

    atualizarGrafico(valorMensal, qtMeses, taxa);
  });
});


// ======================================================
//              FUNÇÃO PARA ATUALIZAR O GRÁFICO
// ======================================================
function atualizarGrafico(valorMensal, meses, taxaMensal) {

  const labels = [];
  const c1 = []; // sem juros
  const c2 = []; // com juros

  let ac1 = 0;
  let ac2 = 0;

  const taxa = taxaMensal / 100;

  for (let i = 1; i <= meses; i++) {
    labels.push(`${i}º mês`);

    ac1 += valorMensal;
    c1.push(ac1);

    ac2 = (ac2 + valorMensal) * (1 + taxa);
    c2.push(ac2);
  }

  const ctx = document.getElementById("graficoSimulacao").getContext("2d");

  if (grafico) grafico.destroy();

  grafico = new Chart(ctx, {
    type: tipoGraficoAtual === "area" ? "line" : tipoGraficoAtual,
    data: {
      labels,
      datasets: [
        {
          label: "Com juros",
          data: c2,
          borderColor: "#00eaff",
          backgroundColor:
            tipoGraficoAtual === "area"
              ? "rgba(0,234,255,0.15)"
              : "transparent",
          borderWidth: 2,
          tension: 0.25,
          pointRadius: 0,
          fill: tipoGraficoAtual === "area",
        },
        {
          label: "Sem juros",
          data: c1,
          borderColor: "#d1d5db",
          backgroundColor:
            tipoGraficoAtual === "area"
              ? "rgba(209,213,219,0.15)"
              : "transparent",
          borderWidth: 2,
          tension: 0.25,
          pointRadius: 0,
          fill: tipoGraficoAtual === "area",
        },
      ],
    },

    options: {
      responsive: true,
      maintainAspectRatio: false,

      animation: {
        duration: 1600,
        easing: "easeOutCubic",
      },

      plugins: {
        legend: {
          labels: {
            color: "#e5e7eb",
            font: { size: 13, weight: "500" },
          },
        },

        tooltip: {
          backgroundColor: "rgba(0,0,0,0.85)",
          borderColor: "#00eaff",
          borderWidth: 1,
          titleColor: "#fff",
          bodyColor: "#e5e7eb",
          padding: 12,
          cornerRadius: 8,
          caretSize: 6,
          callbacks: {
            label: (tooltip) =>
              `${tooltip.dataset.label}: ${formatCurrency(tooltip.raw)}`,
          },
        },
      },

      scales: {
        x: {
          ticks: { color: "#9ca3af" },
          grid: { color: "rgba(255,255,255,0.03)" },
        },
        y: {
          ticks: {
            color: "#9ca3af",
            callback: (v) => v.toLocaleString("pt-BR"),
          },
          grid: { color: "rgba(255,255,255,0.03)" },
        },
      },
    },
  });
}


// ======================================================
// FUNÇÃO PARA ALTERAR O TIPO DE GRÁFICO
// ======================================================
function trocarTipoGrafico(tipo) {
  tipoGraficoAtual = tipo;

  const valorMensal = parseFloat(document.getElementById("valorMensal").value);
  const qtMeses = parseInt(document.getElementById("qtMeses").value, 10);
  const taxa = parseFloat(
    document.getElementById("taxaMensal").value.replace(",", ".")
  ) || 0;

  if (valorMensal && qtMeses) {
    atualizarGrafico(valorMensal, qtMeses, taxa);
  }
}
