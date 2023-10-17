$(document).ready(function () {
    // Función para cargar horas disponibles
    function cargarHorasDisponibles() {
        var rut_med = $("#medicos").val();
        var fecha = $("#fecha").val();

        $.ajax({
            url: 'https://galenos.samgarrido.repl.co/api/agendas/horas',  // Ruta a tu vista de Django que obtiene las horas
            type: 'POST',
            data: {
                'rut_med': rut_med,
                'fecha': fecha
            },
            success: function (data) {
                var selectHoras = $("#hora");
                selectHoras.empty();
                selectHoras.append($('<option>', { value: '', text: 'Selecciona una hora' }));

                for (var i = 0; i < data.hora.length; i++) {
                    selectHoras.append($('<option>', { value: data.hora[i], text: data.hora[i] }));
                }
            },
            error: function () {
                console.log('Error al cargar las horas disponibles.');
            }
        });
    }

    // Escuchar cambios en el combo de médicos y la fecha
    $("#medicos, #fecha").change(cargarHorasDisponibles);
});