// Completa la descripción impresa del presupuesto con la predeterminada según el
// material y la superficie elegidos. Funciona en el modal de creación y en el
// formulario de edición (que se inserta después con fetch), porque escucha en document.

const URL_DESCRIPCION = document.currentScript.dataset.url;

// Último pedido por formulario: si el usuario cambia rápido, se ignoran las respuestas viejas.
const pedidosPendientes = new WeakMap();

function camposDelForm(form) {
  if (!form) return null;
  const material = form.querySelector('select[name="material"]');
  const superficie = form.querySelector('select[name="superficie"]');
  const descripcion = form.querySelector('textarea[name="descripcion_impresa"]');
  if (!material || !superficie || !descripcion) return null;
  return { material, superficie, descripcion };
}

// Solo se reemplaza si está vacía o si todavía tiene el último texto autocompletado:
// si el usuario la editó, se respeta lo que escribió.
function sePuedeReemplazar(descripcion) {
  const actual = descripcion.value.trim();
  return actual === "" || descripcion.value === descripcion.dataset.autocompletado;
}

async function completarDescripcion(form) {
  const campos = camposDelForm(form);
  if (!campos) return;

  const { material, superficie, descripcion } = campos;
  if (!material.value || !superficie.value) return;
  if (!sePuedeReemplazar(descripcion)) return;

  const params = new URLSearchParams({
    material: material.value,
    superficie: superficie.value,
  });
  const pedido = {};
  pedidosPendientes.set(form, pedido);

  try {
    const response = await fetch(`${URL_DESCRIPCION}?${params}`, {
      headers: { "X-Requested-With": "XMLHttpRequest" },
    });
    if (!response.ok) return;
    const { texto } = await response.json();

    // Llegó una respuesta más nueva, o el usuario escribió mientras se esperaba.
    if (pedidosPendientes.get(form) !== pedido) return;
    if (!sePuedeReemplazar(descripcion)) return;

    // Si no hay predeterminada, se limpia el texto autocompletado del par anterior
    // (y si estaba vacía, queda vacía).
    descripcion.value = texto;
    descripcion.dataset.autocompletado = texto;
  } catch (error) {
    // Sin conexión: se deja la descripción como está; el servidor la completa al guardar.
  }
}

document.addEventListener("change", (event) => {
  if (!event.target.matches('select[name="material"], select[name="superficie"]')) return;
  completarDescripcion(event.target.form);
});

// Formularios que ya vienen con material y superficie elegidos al cargar la página
// (por ejemplo, al volver al presupuesto después de crear una obra).
document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll("form").forEach((form) => {
    const campos = camposDelForm(form);
    if (campos && campos.descripcion.value.trim() === "") {
      completarDescripcion(form);
    }
  });
});
