const botones = document.querySelectorAll(".presupuesto__btn");

function abrirModal(modalId) {
  const modal = document.getElementById(modalId);
  if (modal) modal.hidden = false;
}

botones.forEach((boton) => {
  boton.addEventListener("click", () => {
    abrirModal(boton.dataset.modal);
  });
});

const tarjetas = document.querySelectorAll(
  ".presupuestos__mostrar__link[data-modal]",
);

tarjetas.forEach((tarjeta) => {
  tarjeta.addEventListener("click", (event) => {
    if (event.target.closest("button, a")) return;
    abrirModal(tarjeta.dataset.modal);
  });

  tarjeta.addEventListener("keydown", (event) => {
    if (event.key === "Enter" || event.key === " ") {
      event.preventDefault();
      abrirModal(tarjeta.dataset.modal);
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

const modales = document.querySelectorAll(".presupuesto__modal");

modales.forEach((modal) => {
  modal.addEventListener("click", (event) => {
    if (event.target === modal) modal.hidden = true;
  });
});

document.addEventListener("keydown", (event) => {
  if (event.key === "Escape") {
    modales.forEach((modal) => {
      modal.hidden = true;
    });
  }
});
