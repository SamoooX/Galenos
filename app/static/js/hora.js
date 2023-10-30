$(document).ready(function () {
    // Función para cargar horas disponibles
    function cargarHorasDisponibles() {
        var rut_med = $("#medicos").val();
        var fecha = $("#fecha").val();

        $.ajax({
            url: 'https://galenos.samgarrido.repl.co/api/agendas/horas',
            type: 'POST',
            data: JSON.stringify({
                'rut_med': rut_med,
                'fecha': fecha
            }),
            contentType: 'application/json',
            success: function (data) {
                var selectHoras = $("#hora");
                selectHoras.empty();
                selectHoras.append($('<option>', { value: '', text: 'Selecciona una hora' }));

                for (var i = 0; i < data.hora.length; i++) {
                    selectHoras.append($('<option>', { value: data.hora[i], text: data.hora[i] }));
                }
            },
            error: function (xhr, status, error) {
                console.log('Error al cargar las horas disponibles.');
                console.log(error); // Puedes imprimir información adicional sobre el error en la consola
            }
        });
    }

    // Escuchar cambios en el combo de médicos y la fecha
    $("#medicos, #fecha").change(cargarHorasDisponibles);

    function cancelarAgenda(rut_med, fecha, hora) {
        $.ajax({
            url: 'https://galenos.samgarrido.repl.co/api/agendas/disponibilidad',
            type: 'PATCH',
            data: JSON.stringify({
                'rut_med': rut_med,
                'fecha': fecha,
                'hora': hora,
                'disponibilidad': false
            }),
            contentType: 'application/json',
            success: function (response) {
                // Manejar la respuesta del servidor si es necesario
                console.log('Cancelado exitosamente:', response);
            },
            error: function (error) {
                console.log('Error al enviar los datos.');
                console.log(error); // Puedes imprimir información adicional sobre el error en la consola
            }
        });
    }

    function enviarDatos() {
        var rut_pac = $("#rut").val(); // Obtener el valor de rut del paciente
        var rut_med = $("#medicos").val(); // Obtener el valor del médico
        var fecha = $("#fecha").val(); // Obtener el valor de la fecha
        var hora = $("#hora").val(); // Obtener el valor de la hora

        console.log(rut_pac)
        console.log(rut_med)
        console.log(fecha)
        console.log(hora)
        // Crear un objeto JSON con los datos a enviar
        var datos = {
            'fecha': fecha,
            'hora': hora,
            'rut_med': rut_med,
            'rut_pac': rut_pac,
            'rut_sec': 728364152,
            'costo' : 15000,
            'estado' : false,
            'cancelado' : false
        };

        // Enviar los datos al servidor en formato JSON
        $.ajax({
            url: 'https://galenos.samgarrido.repl.co/api/atenciones/add', // Reemplaza con la URL correcta de tu API
            type: 'POST',
            data: JSON.stringify(datos),
            contentType: 'application/json',
            success: function (response) {
                // Manejar la respuesta del servidor si es necesario
                cancelarAgenda(rut_med, fecha, hora);
                console.log('Datos enviados exitosamente:', response);
            },
            error: function (xhr, status, error) {
                console.log('Error al enviar los datos.');
                console.log(error); // Puedes imprimir información adicional sobre el error en la consola
            }
        });
    }

    // Asociar la función al evento de envío del formulario
    $("#reserva-form").on("submit", function (event) {
        event.preventDefault(); // Prevenir el envío del formulario por defecto
        enviarDatos(); // Llamar a la función para enviar los datos
    });


});