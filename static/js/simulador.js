function formatCurrency(valor) {
  return valor.toLocaleString("pt-BR", {
    style: "currency",
    currency: "BRL",
    maximumFractionDigits: 2
  });
}

document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("simulador-form");
  const resultadoCard = document.getElementById("resultado");
  const totalSemJurosEl = document.getElementById("totalSemJuros");
  const totalComJurosEl = document.getElementById("totalComJuros");
  const textoDiferencaEl = document.getElementById("textoDiferenca");

  form.addEventListener("submit", (event) => {
    event.preventDefault();

    const valorMensal = parseFloat(
      document.getElementById("valorMensal").value.replace(",", ".")
    );
    const qtMeses = parseInt(
      document.getElementById("qtMeses").value,
      10
    );
    const taxaInput = document
      .getElementById("taxaMensal")
      .value.replace(",", ".");

    const taxaMensal = taxaInput ? parseFloat(taxaInput) / 100 : 0;

    if (isNaN(valorMensal) || isNaN(qtMeses) || valorMensal <= 0 || qtMeses <= 0) {
      alert("Preencha os campos obrigatórios com valores válidos.");
      return;
    }

    const totalSemJuros = valorMensal * qtMeses;

    let totalComJuros = totalSemJuros;
    if (taxaMensal > 0) {
      totalComJuros = valorMensal * ((Math.pow(1 + taxaMensal, qtMeses) - 1) / taxaMensal);
    }

    const diferenca = totalComJuros - totalSemJuros;

    totalSemJurosEl.textContent = formatCurrency(totalSemJuros);
    totalComJurosEl.textContent = formatCurrency(totalComJuros);

    if (taxaMensal > 0 && diferenca > 0) {
      textoDiferencaEl.textContent =
        `Só em juros, você ganhou aproximadamente ${formatCurrency(diferenca)} ` +
        `ao longo de ${qtMeses} meses. É o poder dos juros compostos trabalhando por você.`;
    } else {
      textoDiferencaEl.textContent =
        "Aqui você está vendo apenas a soma dos depósitos mensais, sem considerar rendimento.";
    }

    // Mostra o card de resultado com transição
    resultadoCard.classList.remove("result-card--hidden");
  });
});
