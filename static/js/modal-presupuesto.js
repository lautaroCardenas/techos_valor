const modal = document.getElementById("presupuesto__modal");
const abrirModal = document.getElementById("modal__abrir");
const cerrarModal = document.getElementById("modal__cerrar");

if (modal && abrirModal && cerrarModal) {
  abrirModal.addEventListener("click", () => {
    modal.hidden = false;
  });

  cerrarModal.addEventListener("click", () => {
    modal.hidden = true;
  });

  modal.addEventListener("click", (event) => {
    if (event.target === modal) {
      modal.hidden = true;
    }
  });

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape") {
      modal.hidden = true;
    }
  });
}
