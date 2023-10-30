$(document).ready(function() {
    $("#cambiar-disponibilidad").on("click", function() {
      // Crear una lista para almacenar los datos seleccionados
      var seleccionados = [];
  
      // Iterar sobre los checkboxes marcados
      $(".agenda-checkbox:checked").each(function() {
        var fecha = $(this).data("fecha");
        var hora = $(this).data("hora");
        console.log(fecha);
        console.log(hora);
        // Agregar los datos al array seleccionados
        seleccionados.push({ rut_med: "123456789", fecha: fecha, hora: hora, disponibilidad: false });
      });
      console.log(JSON.stringify(seleccionados));
      // Realizar una solicitud a la API con los datos seleccionados
      $.ajax({
        url: 'https://galenos.samgarrido.repl.co/api/agendas/disponibilidad', // Reemplaza con la URL correcta de tu API
        type: 'PATCH',
        data: JSON.stringify(seleccionados),
        contentType: 'application/json',
        success: function(response) {
          // Manejar la respuesta de la API si es necesario
          console.log('Cambios de disponibilidad realizados:', response);
        },
        error: function(error) {
          console.log('Error al cambiar la disponibilidad.');
          console.log(error);
        }
      });
    });
  });