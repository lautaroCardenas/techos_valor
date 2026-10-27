const formularioObra = document.getElementById("obra__form");
const formularioPresupuesto = document.querySelector(".presupuestonuevo form");
const formularioCliente = document.getElementById("cliente__form");
const modalCliente = document.getElementById("cliente__modal");
const abrirCliente = document.getElementById("modal__abrir__cliente");
const cerrarCliente = document.getElementById("modal__cerrar__cliente");

if (modalCliente && abrirCliente && cerrarCliente) {
  abrirCliente.addEventListener("click", () => {
    modalCliente.hidden = false;
  });

  cerrarCliente.addEventListener("click", () => {
    modalCliente.hidden = true;
  });

  modalCliente.addEventListener("click", (event) => {
    if (event.target === modalCliente) {
      modalCliente.hidden = true;
    }
  });

  if (modalCliente.dataset.abrir === "true") {
    modalCliente.hidden = false;
  }
}

function copiarCampos(origen, destino, prefijo) {
  if (!origen || !destino) return;

  destino
    .querySelectorAll(`[data-pendiente="${prefijo}"]`)
    .forEach((campo) => campo.remove());

  for (const campo of origen.elements) {
    if (!campo.name || campo.name === "csrfmiddlewaretoken") continue;

    const oculto = document.createElement("input");
    oculto.type = "hidden";
    oculto.name = `${prefijo}${campo.name}`;
    oculto.value =
      campo.type === "checkbox" ? (campo.checked ? "on" : "") : campo.value;

    oculto.dataset.pendiente = prefijo;
    destino.appendChild(oculto);
  }
}

if (formularioCliente) {
  formularioCliente.addEventListener("submit", () => {
    const origen = formularioCliente.querySelector('[name="origen"]');
    if (origen) {
      origen.value = formularioPresupuesto ? "presupuestos" : "obra_crear";
    }

    copiarCampos(formularioObra, formularioCliente, "obra__");
    copiarCampos(formularioPresupuesto, formularioCliente, "presupuesto__");
  });
}

if (formularioObra) {
  formularioObra.addEventListener("submit", () => {
    const origen = formularioObra.querySelector('[name="origen"]');
    if (formularioPresupuesto) {
      if (origen) origen.value = "presupuestos";
      copiarCampos(formularioPresupuesto, formularioObra, "presupuesto__");
    }
  });
}
