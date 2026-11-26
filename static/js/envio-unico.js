// Evita enviar dos veces el mismo formulario (doble clic, Enter repetido) mientras la
// página carga: al enviar se deshabilita el botón y se ignoran los envíos siguientes.
// El servidor también lo controla (servicios/envio_unico.py); esto es para que se vea.

document.addEventListener("submit", (event) => {
  const form = event.target;

  // Los formularios que se mandan con fetch (por ejemplo, editar presupuesto) cancelan
  // el envío normal y manejan su propio botón.
  if (event.defaultPrevented) return;
  if ((form.getAttribute("method") || "get").toLowerCase() !== "post") return;

  if (form.dataset.enviando === "true") {
    event.preventDefault();
    return;
  }
  form.dataset.enviando = "true";

  // Se deshabilita después de que el navegador arme los datos del envío.
  setTimeout(() => {
    form.querySelectorAll('button[type="submit"], button:not([type]), input[type="submit"]').forEach((boton) => {
      boton.disabled = true;
      // Solo se cambia el texto de los botones con texto (no los de ícono, como la X de borrar).
      if (boton.tagName === "BUTTON" && boton.children.length === 0 && boton.textContent.trim()) {
        boton.dataset.textoOriginal = boton.textContent;
        boton.textContent = boton.dataset.textoEnviando || "Guardando…";
      }
    });
  }, 0);
});

// Al volver con "Atrás", el navegador puede mostrar la página como quedó: se reactivan.
window.addEventListener("pageshow", (event) => {
  if (!event.persisted) return;
  document.querySelectorAll('form[data-enviando="true"]').forEach((form) => {
    form.dataset.enviando = "false";
    form.querySelectorAll("button, input[type='submit']").forEach((boton) => {
      boton.disabled = false;
      if (boton.dataset.textoOriginal) boton.textContent = boton.dataset.textoOriginal;
    });
  });
});

// Carteles de "cargado correctamente": se cierran solos o al tocarlos.
document.querySelectorAll(".aviso").forEach((aviso, indice) => {
  const cerrar = () => {
    aviso.classList.add("aviso--saliendo");
    aviso.addEventListener("animationend", () => aviso.remove(), { once: true });
  };
  aviso.addEventListener("click", cerrar);
  setTimeout(cerrar, 3500 + indice * 500);
});
