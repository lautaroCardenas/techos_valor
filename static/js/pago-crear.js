document.addEventListener("DOMContentLoaded", () => {
  const modal = document.getElementById("pago-modal");
  const cerrar = document.getElementById("pago-modal-cerrar");
  const presupuestoInput = document.getElementById("pago-presupuesto-id");
  const botones = document.querySelectorAll(".js-agregar-pago");

  if (!modal || !cerrar || !presupuestoInput) return;

  botones.forEach((boton) => {
    boton.addEventListener("click", () => {
      presupuestoInput.value = boton.dataset.presupuestoId;
      modal.showModal();
    });
  });

  cerrar.addEventListener("click", () => {
    modal.close();
  });

  if (modal.dataset.open === "true") {
    modal.showModal();
  }

  modal.addEventListener("click", (event) => {
    if (event.target === modal) {
      modal.close();
    }
  });
});
