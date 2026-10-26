const botones = document.querySelectorAll(".presupuesto__btn");

botones.forEach((boton) => {
  boton.addEventListener("click", () => {
    const modalId = boton.dataset.modal;
    const modal = document.getElementById(modalId);

    if (modal) {
      modal.hidden = false;
    }
  });
});

const botonesCerrar = document.querySelectorAll(".presupuesto__modal__cerrar");

botonesCerrar.forEach((boton) => {
  boton.addEventListener("click", () => {
    const modal = boton.closest(".presupuesto__modal");

    if (modal) {
      modal.hidden = true;
    }
  });
});
