document.addEventListener("click", (event) => {
  const agregar = event.target.closest("[data-visitas-agregar]");

  if (agregar) {
    const bloque = agregar.closest("[data-visitas]");
    const total = bloque.querySelector('input[name$="-TOTAL_FORMS"]');
    const plantilla = bloque.querySelector("template");
    const lista = bloque.querySelector("[data-visitas-lista]");

    const indice = parseInt(total.value, 10);
    lista.insertAdjacentHTML(
      "beforeend",
      plantilla.innerHTML.replaceAll("__prefix__", indice),
    );
    total.value = indice + 1;
    return;
  }

  const quitar = event.target.closest("[data-visitas-quitar]");

  if (quitar) {
    const fila = quitar.closest(".visita-form");
    const fecha = fila.querySelector('input[type="date"]');
    if (fecha) fecha.value = "";
    fila.hidden = true;
  }
});
