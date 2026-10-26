const formularioPresupuesto = document.querySelector(".presupuestonuevo form");
const formularioObra = document.getElementById("obra__form");

if (formularioPresupuesto && formularioObra) {
  formularioObra.addEventListener("submit", () => {
    formularioObra
      .querySelectorAll("[data-presupuesto-pendiente]")
      .forEach((campo) => campo.remove());

    const campos = [
      "metro_2",
      "precio_metro",
      "material",
      "superficie",
      "obra",
      "observacion",
      "recargo_porcentaje",
      "descripcion_impresa",
    ];

    campos.forEach((nombre) => {
      const campo = formularioPresupuesto.elements.namedItem(nombre);

      if (!campo) return;

      const oculto = document.createElement("input");
      oculto.type = "hidden";
      oculto.name = `presupuesto__${nombre}`;
      oculto.value = campo.value;
      oculto.dataset.presupuestoPendiente = "true";

      formularioObra.appendChild(oculto);
    });
  });
}
