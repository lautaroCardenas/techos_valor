const botones = document.querySelectorAll(
  ".presupuesto__btn, .obradetalle__presupuesto__btn",
);

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

const botonesEditar = document.querySelectorAll("[data-editar-presupuesto]");

botonesEditar.forEach((boton) => {
  boton.addEventListener("click", async () => {
    const modal = boton.closest(".presupuesto__modal");

    const detalle = modal.querySelector(".presupuesto__detalle");

    const edicion = modal.querySelector(".presupuesto__edicion");

    detalle.hidden = true;
    edicion.hidden = false;

    // Si ya se cargó, no volver a solicitarlo.
    if (edicion.dataset.cargado === "true") return;

    try {
      const response = await fetch(edicion.dataset.formUrl);

      if (!response.ok) {
        throw new Error("No se pudo cargar el formulario");
      }

      edicion.innerHTML = await response.text();
      edicion.dataset.cargado = "true";
    } catch (error) {
      edicion.innerHTML = `
        <p>No se pudo cargar el formulario.</p>
        <button type="button" class="presupuesto__volver">
          Volver
        </button>
      `;
    }
  });
});

document.addEventListener("submit", async (event) => {
  const form = event.target.closest(".presupuesto__form__editar");

  if (!form) return;

  event.preventDefault();

  const modal = form.closest(".presupuesto__modal");
  const detalle = modal.querySelector(".presupuesto__detalle");
  const edicion = modal.querySelector(".presupuesto__edicion");

  const botonGuardar = form.querySelector('button[type="submit"]');

  botonGuardar.disabled = true;
  botonGuardar.textContent = "Guardando...";

  try {
    const response = await fetch(form.action, {
      method: "POST",
      body: new FormData(form),
      headers: {
        "X-Requested-With": "XMLHttpRequest",
      },
    });

    const html = await response.text();

    if (!response.ok) {
      edicion.innerHTML = html;
      return;
    }

    detalle.innerHTML = html;
    edicion.hidden = true;
    detalle.hidden = false;

    edicion.innerHTML = "";
    edicion.dataset.cargado = "false";
  } catch (error) {
    alert("Ocurrió un error al guardar el presupuesto.");
  } finally {
    botonGuardar.disabled = false;
  }
});

document.addEventListener("click", (event) => {
  const boton = event.target.closest(".presupuesto__cancelar__editar");

  if (!boton) return;

  const modal = boton.closest(".presupuesto__modal");

  const detalle = modal.querySelector(".presupuesto__detalle");

  const edicion = modal.querySelector(".presupuesto__edicion");

  edicion.hidden = true;
  detalle.hidden = false;
});
