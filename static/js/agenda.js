document.addEventListener("DOMContentLoaded", () => {
  const el = document.getElementById("calendario");
  if (!el) return;

  const dialogo = document.getElementById("dialogo-evento");
  const form = document.getElementById("form-evento");
  const errores = document.getElementById("errores-evento");
  const titulo = document.getElementById("titulo-dialogo");
  const btnEliminar = document.getElementById("eliminar-evento");
  const csrf = () => form.elements["csrfmiddlewaretoken"].value;

  // Reemplaza el 0 de relleno por el id real
  const urlConId = (base, id) => base.replace("/0/", `/${id}/`);

  let eventoActual = null; // null = creando, objeto = editando

  async function post(url, body) {
    const resp = await fetch(url, {
      method: "POST",
      headers: { "X-CSRFToken": csrf() },
      body,
    });
    return { resp, data: await resp.json() };
  }

  function abrirDialogo(evento = null, fechaInicial = "") {
    eventoActual = evento;
    form.reset();
    errores.textContent = "";

    if (evento) {
      const p = evento.extendedProps;
      titulo.textContent = "Editar evento";
      form.elements["titulo"].value = evento.title;
      form.elements["fecha"].value = p.fecha;
      form.elements["tipo"].value = p.tipo ?? "";
      form.elements["estado"].value = p.estado ?? "";
      form.elements["obra"].value = p.obra ?? "";
      form.elements["descripcion"].value = p.descripcion;
      btnEliminar.hidden = false;
    } else {
      titulo.textContent = "Nuevo evento";
      form.elements["fecha"].value = fechaInicial;
      btnEliminar.hidden = true;
    }
    dialogo.showModal();
  }

  const calendar = new FullCalendar.Calendar(el, {
    initialView: "dayGridMonth",
    locale: "es",
    timeZone: "UTC",
    editable: true,
    eventDurationEditable: false, // no hay fecha_fin, solo se mueve
    headerToolbar: {
      left: "prev,next today",
      center: "title",
      right: "dayGridMonth,timeGridWeek,timeGridDay,listWeek",
    },
    events: el.dataset.eventsUrl,

    // CREAR
    dateClick: (info) => {
      const dia = info.dateStr.slice(0, 10);
      const hora = info.allDay ? "09:00" : info.dateStr.slice(11, 16);
      abrirDialogo(null, `${dia}T${hora}`);
    },

    // EDITAR / ELIMINAR
    eventClick: (info) => {
      info.jsEvent.preventDefault();
      abrirDialogo(info.event);
    },

    // MOVER (arrastrar)
    eventDrop: async (info) => {
      // Con timeZone "UTC", los campos UTC son la hora local argentina
      const fecha = info.event.start.toISOString().slice(0, 16);
      const body = new FormData();
      body.append("fecha", fecha);

      const { resp, data } = await post(
        urlConId(el.dataset.moveUrl, info.event.id),
        body,
      );
      if (!resp.ok) {
        alert(data.error || "No se pudo mover el evento.");
        info.revert(); // vuelve a la posición original
      } else {
        calendar.refetchEvents();
      }
    },
  });
  calendar.render();
  document
    .getElementById("btn-agregar-evento")
    .addEventListener("click", () => {
      abrirDialogo(null, "");
    });

  document
    .getElementById("cancelar-evento")
    .addEventListener("click", () => dialogo.close());

  // CREAR o EDITAR (según eventoActual)
  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const url = eventoActual
      ? urlConId(el.dataset.updateUrl, eventoActual.id)
      : el.dataset.createUrl;

    const { data } = await post(url, new FormData(form));
    if (data.ok) {
      dialogo.close();
      calendar.refetchEvents();
    } else {
      errores.textContent = Object.values(data.errors)
        .flat()
        .map((err) => err.message)
        .join(" ");
    }
  });

  // ELIMINAR
  btnEliminar.addEventListener("click", async () => {
    if (!eventoActual || !confirm("¿Eliminar este evento?")) return;
    const { data } = await post(
      urlConId(el.dataset.deleteUrl, eventoActual.id),
      new FormData(),
    );
    if (data.ok) {
      dialogo.close();
      calendar.refetchEvents();
    }
  });
});
