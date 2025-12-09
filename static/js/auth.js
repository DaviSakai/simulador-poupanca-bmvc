// AUTH UX – toggle de senha, validação leve e botão com loading

document.addEventListener("DOMContentLoaded", () => {
    /* ==========================
       TOGGLE DE SENHA (SIMPLES E ROBUSTO)
    ========================== */
    document.querySelectorAll(".password-box").forEach((box) => {
        const input = box.querySelector("input");
        const toggle = box.querySelector(".toggle-password");
        if (!input || !toggle) return;

        toggle.addEventListener("click", (e) => {
            e.preventDefault();

            const isPassword = input.type === "password";
            input.type = isPassword ? "text" : "password";

            // classe visual do ícone
            if (isPassword) {
                toggle.classList.add("is-active");
            } else {
                toggle.classList.remove("is-active");
            }
        });
    });

    /* ==========================
       VALIDAÇÃO VISUAL LEVE
    ========================== */
    const markField = (input) => {
        if (!input) return;
        const value = input.value.trim();

        input.classList.remove("valid", "invalid");

        if (!value) {
            input.classList.add("invalid");
        } else if (value.length >= 3) {
            input.classList.add("valid");
        }
    };

    document.querySelectorAll(".premium-input").forEach((input) => {
        // quando o usuário sai do campo
        input.addEventListener("blur", () => markField(input));

        // enquanto digita, se já tiver sido marcado
        input.addEventListener("input", () => {
            if (
                input.classList.contains("invalid") ||
                input.classList.contains("valid")
            ) {
                markField(input);
            }
        });
    });

    /* ==========================
       SUBMIT + BOTÃO COM LOADING
    ========================== */
    document.querySelectorAll(".premium-form").forEach((form) => {
        form.addEventListener("submit", (event) => {
            const inputs = form.querySelectorAll(".premium-input[required]");
            let hasError = false;

            inputs.forEach((inp) => {
                const value = inp.value.trim();
                if (!value) {
                    inp.classList.add("invalid");
                    hasError = true;
                }
            });

            if (hasError) {
                // animação de "shake" no form
                form.classList.add("form-shake");
                const firstError = form.querySelector(".premium-input.invalid");
                if (firstError) firstError.focus();

                setTimeout(() => form.classList.remove("form-shake"), 350);
                event.preventDefault();
                return;
            }

            const btn = form.querySelector(".premium-btn");
            if (!btn || btn.classList.contains("is-loading")) return;

            btn.classList.add("is-loading");
            btn.disabled = true;

            const originalText = btn.textContent;
            btn.dataset.originalText = originalText;

            if (/entrar/i.test(originalText)) {
                btn.textContent = "Entrando...";
            } else if (/criar/i.test(originalText)) {
                btn.textContent = "Criando conta...";
            } else {
                btn.textContent = "Processando...";
            }
        });
    });
});
