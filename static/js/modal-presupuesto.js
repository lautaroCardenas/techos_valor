const modalPresupuesto = document.getElementById("presupuesto__modal");
const abrirPresupuesto = document.getElementById("modal__abrir");
const cerrarPresupuesto = document.getElementById("modal__cerrar");

const modalObra = document.getElementById("obra__modal");
const abrirObra = document.getElementById("modal__abrir__obra");
const cerrarObra = document.getElementById("modal__cerrar__obra");

if (modalPresupuesto && abrirPresupuesto && cerrarPresupuesto) {
  abrirPresupuesto.addEventListener("click", () => {
    modalPresupuesto.hidden = false;
  });

  cerrarPresupuesto.addEventListener("click", () => {
    modalPresupuesto.hidden = true;
  });

  modalPresupuesto.addEventListener("click", (event) => {
    if (event.target === modalPresupuesto) {
      modalPresupuesto.hidden = true;
    }
  });
}

if (modalObra && abrirObra && cerrarObra) {
  abrirObra.addEventListener("click", (event) => {
    event.preventDefault();
    event.stopPropagation();

    modalObra.hidden = false;
  });

  cerrarObra.addEventListener("click", (event) => {
    event.preventDefault();
    event.stopPropagation();

    modalObra.hidden = true;
  });

  modalObra.addEventListener("click", (event) => {
    if (event.target === modalObra) {
      modalObra.hidden = true;
    }
  });
}

document.addEventListener("keydown", (event) => {
  if (event.key === "Escape") {
    if (modalObra && !modalObra.hidden) {
      modalObra.hidden = true;
    } else if (modalPresupuesto && !modalPresupuesto.hidden) {
      modalPresupuesto.hidden = true;
    }
  }
});
