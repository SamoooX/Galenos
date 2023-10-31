$(document).ready(function() {
  $("#no-disponible").on("click", function() {
      // Iterar sobre los checkboxes marcados
      $(".agenda-checkbox:checked").each(function() {
          var rut = $(this).data("rut");
          var fecha = $(this).data("fecha");
          var hora = $(this).data("hora");

          // Crear un objeto con los datos de la fecha actual
          var data = {
              rut_med: rut +"",
              fecha: fecha,
              hora: hora,
              disponibilidad: false
          };

          // Realizar una solicitud PATCH para cambiar la disponibilidad
          $.ajax({
              url: 'https://galenos.samgarrido.repl.co/api/agendas/disponibilidad', // URL de la API
              type: 'PATCH',
              data: JSON.stringify(data),
              contentType: 'application/json',
              success: function(response) {
                  // Manejar la respuesta de la API si es necesario
                  console.log('Cambio de disponibilidad realizado para fecha:', fecha);
              },
              error: function(error) {
                  console.log('Error al cambiar la disponibilidad para fecha:', fecha);
                  console.log(error);
              }
          });
      });
  });

  $("#disponible").on("click", function() {
    // Iterar sobre los checkboxes marcados
    $(".agenda-checkbox:checked").each(function() {
        var rut = $(this).data("rut");
        var fecha = $(this).data("fecha");
        var hora = $(this).data("hora");

        // Crear un objeto con los datos de la fecha actual
        var data = {
            rut_med: rut +"",
            fecha: fecha,
            hora: hora,
            disponibilidad: true
        };

        // Realizar una solicitud PATCH para cambiar la disponibilidad
        $.ajax({
            url: 'https://galenos.samgarrido.repl.co/api/agendas/disponibilidad', // URL de la API
            type: 'PATCH',
            data: JSON.stringify(data),
            contentType: 'application/json',
            success: function(response) {
                // Manejar la respuesta de la API si es necesario
                console.log('Cambio de disponibilidad realizado para fecha:', fecha);
            },
            error: function(error) {
                console.log('Error al cambiar la disponibilidad para fecha:', fecha);
                console.log(error);
            }
        });
    });
});
});