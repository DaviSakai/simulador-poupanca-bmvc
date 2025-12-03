function formatarMoeda(v) {
  return v.toLocaleString("pt-BR", { style:"currency", currency:"BRL" });
}

function limpar(v) {
  if (!v) return 0;
  return Number(v.replace(",", "."));
}

document.getElementById("btnCalcular").addEventListener("click", () => {
  
  const valor = limpar(document.getElementById("valor_mensal").value);
  const meses = limpar(document.getElementById("qt_meses").value);
  const jurosAno = limpar(document.getElementById("taxa_juros").value) / 100;

  const preview = document.getElementById("preview-box");
  const pInvest = document.getElementById("p_invest");
  const pJuros = document.getElementById("p_juros");
  const pTotal = document.getElementById("p_total");

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
      const jurosMes = (1 + jurosAno) ** (1/12) - 1;
      for (let i = 0; i < meses; i++) {
          total += valor * jurosMes * (meses - i);
      }
  }

  const ganho = total - investido;

  pInvest.textContent = "Você investirá: " + formatarMoeda(investido);
  pJuros.textContent = "Com juros estimados: " + formatarMoeda(ganho);
  pTotal.innerHTML = "<b>Total final estimado: " + formatarMoeda(total) + "</b>";

  preview.style.display = "block";
});
