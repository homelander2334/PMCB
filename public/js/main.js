document.addEventListener("DOMContentLoaded", () => {
  const menuToggle = document.getElementById("menuToggle");
  const mainNav = document.getElementById("mainNav");
  const currentYear = document.getElementById("currentYear");

  if (currentYear) {
    currentYear.textContent = new Date().getFullYear();
  }

  if (menuToggle && mainNav) {
    function closeMenu() {
      mainNav.classList.remove("is-open");
      menuToggle.setAttribute("aria-expanded", "false");
      menuToggle.setAttribute("aria-label", "Abrir menu");
    }

    function toggleMenu() {
      const isOpen = mainNav.classList.toggle("is-open");
      menuToggle.setAttribute("aria-expanded", String(isOpen));
      menuToggle.setAttribute(
        "aria-label",
        isOpen ? "Fechar menu" : "Abrir menu"
      );
    }

    menuToggle.addEventListener("click", toggleMenu);
    mainNav.querySelectorAll("a").forEach(link => {
      link.addEventListener("click", closeMenu);
    });

    document.addEventListener("keydown", event => {
      if (event.key === "Escape") closeMenu();
    });

    document.addEventListener("click", event => {
      if (
        mainNav.classList.contains("is-open") &&
        !mainNav.contains(event.target) &&
        !menuToggle.contains(event.target)
      ) {
        closeMenu();
      }
    });
  }

  document.querySelectorAll(".participation-form").forEach(form => {
    form.addEventListener("submit", async event => {
      event.preventDefault();

      const button = form.querySelector('button[type="submit"]');
      const status = form.querySelector(".form-status");
      const originalText = button.textContent;

      button.disabled = true;
      button.textContent = "Enviando...";
      status.textContent = "";

      try {
        const csrfResponse = await fetch("/api/csrf", {
          credentials: "same-origin"
        });

        if (!csrfResponse.ok) {
          throw new Error("Não foi possível preparar o envio.");
        }

        const csrfData = await csrfResponse.json();

        const data = Object.fromEntries(new FormData(form).entries());
        data.privacy_consent = form.elements.privacy_consent.checked;

        const response = await fetch(form.dataset.endpoint, {
          method: "POST",
          credentials: "same-origin",
          headers: {
            "Content-Type": "application/json",
            "x-csrf-token": csrfData.csrfToken
          },
          body: JSON.stringify(data)
        });

        const result = await response.json();

        if (!response.ok || !result.success) {
          throw new Error(result.message || "Não foi possível enviar.");
        }

        status.textContent = result.message;
        form.reset();
      } catch (error) {
        status.textContent = error.message ||
          "Erro de conexão. Tente novamente.";
      } finally {
        button.disabled = false;
        button.textContent = originalText;
      }
    });
  });
});
