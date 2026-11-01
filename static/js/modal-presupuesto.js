const modalPresupuesto = document.getElementById("presupuesto__modal");
const abrirPresupuesto = document.getElementById("modal__abrir");
const cerrarPresupuesto = document.getElementById("modal__cerrar");
const panelPresupuesto = document.getElementById("presupuesto__panel");
const panelObra = document.getElementById("obra__panel");
const abrirObra = document.getElementById("modal__abrir__obra");
const volverPresupuesto = document.getElementById("modal__volver__presupuesto");
const modalConfirmacion = document.getElementById("modal__confirmacion");
const botonesBorrar = document.querySelectorAll(".presupuesto__btn__delete");
const botonCancelar = document.getElementById("cancelar__borrar");
const formBorrar = document.getElementById("form__borrar");

function mostrarPanel(panelActivo) {
  if (!panelPresupuesto || !panelObra) return;

  panelPresupuesto.hidden = panelActivo !== panelPresupuesto;
  panelObra.hidden = panelActivo !== panelObra;
}

if (modalPresupuesto && abrirPresupuesto && cerrarPresupuesto) {
  abrirPresupuesto.addEventListener("click", () => {
    mostrarPanel(panelPresupuesto);
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

if (abrirObra) {
  abrirObra.addEventListener("click", () => {
    mostrarPanel(panelObra);
  });
}

if (volverPresupuesto) {
  volverPresupuesto.addEventListener("click", () => {
    mostrarPanel(panelPresupuesto);
  });
}

const modalState = document.getElementById("modal-state");
if (modalState && modalPresupuesto) {
  const abrirObraInicial = modalState.dataset.abrirObra === "true";
  const abrirPresupuestoInicial =
    modalState.dataset.abrirPresupuesto === "true";

  if (abrirObraInicial || abrirPresupuestoInicial) {
    modalPresupuesto.hidden = false;
    mostrarPanel(abrirObraInicial ? panelObra : panelPresupuesto);
  }
}

document.addEventListener("keydown", (event) => {
  if (event.key === "Escape") {
    if (modalPresupuesto && !modalPresupuesto.hidden) {
      modalPresupuesto.hidden = true;
    }
  }
});

botonesBorrar.forEach((boton) => {
  boton.addEventListener("click", () => {
    const presupuestoId = boton.dataset.presupuesto;

    if (!formBorrar || !modalConfirmacion) return;

    formBorrar.action = `/presupuestos/borrar/${presupuestoId}/`;

    modalConfirmacion.hidden = false;
  });
});

if (botonCancelar && modalConfirmacion) {
  botonCancelar.addEventListener("click", () => {
    modalConfirmacion.hidden = true;
  });

  modalConfirmacion.addEventListener("click", (event) => {
    if (event.target === modalConfirmacion) {
      modalConfirmacion.hidden = true;
    }
  });
}

document.addEventListener("keydown", (event) => {
  if (event.key === "Escape" && modalConfirmacion) {
    modalConfirmacion.hidden = true;
  }
});
