function togglePassword() {
    const input = document.getElementById("password");
    if (!input) return;

    const isPassword = input.type === "password";
    input.type = isPassword ? "text" : "password";
}

// Microinteração no submit (botão entra em "estado carregando")
document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("login-form");
    const button = document.getElementById("login-button");

    if (!form || !button) return;

    form.addEventListener("submit", () => {
        button.classList.add("is-loading");
        button.textContent = "Entrando...";
    });
});
