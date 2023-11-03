$(document).ready(function() {
    $("#atendido").on("click", function() {
        // Iterar sobre los checkboxes marcados
        $(".agenda-checkbox:checked").each(function() {
            var rut_med = $(this).data("rut_med");
            var rut_pac = $(this).data("rut_pac");
            var fecha = $(this).data("fecha");
            var hora = $(this).data("hora");
  
            // Crear un objeto con los datos de la fecha actual
            var data = {
                rut_med: rut_med +"",
                rut_pac: rut_pac +"",
                fecha: fecha,
                hora: hora
            };
  
            // Realizar una solicitud PATCH para cambiar la disponibilidad
            $.ajax({
                url: 'https://galenos.samgarrido.repl.co/api/atenciones/estado', // URL de la API
                type: 'PATCH',
                data: JSON.stringify(data),
                contentType: 'application/json',
                success: function(response) {
                    // Manejar la respuesta de la API si es necesario
                    console.log('Cambio de atencion realizado para :', rut_pac);
                },
                error: function(error) {
                    console.log('Error al cambiar la atencion para :', rut_pac);
                    console.log(error);
                }
            });
        });
    });
  
});