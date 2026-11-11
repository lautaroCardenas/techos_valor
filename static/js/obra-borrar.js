const modalObras = document.getElementById("modal__confirmacion");
const botonesBorrarObras = document.querySelectorAll(
  ".obras__acciones__borrar",
);
const botonCancelarObras = document.getElementById("cancelar__borrar");
const formBorrarObras = document.getElementById("form__borrar");

botonesBorrarObras.forEach((botonObra) => {
  botonObra.addEventListener("click", (event) => {
    event.preventDefault();
    event.stopPropagation();

    const obraId = botonObra.dataset.obra;

    if (!obraId || !formBorrarObras || !modalObras) return;

    formBorrarObras.action = `/obras/borrar/${obraId}/`;
    modalObras.hidden = false;
  });
});

if (botonCancelarObras && modalObras) {
  botonCancelarObras.addEventListener("click", () => {
    modalObras.hidden = true;
  });

  modalObras.addEventListener("click", (event) => {
    if (event.target === modalObras) {
      modalObras.hidden = true;
    }
  });
}

document.addEventListener("keydown", (event) => {
  if (event.key === "Escape" && modalObras) {
    modalObras.hidden = true;
  }
});
