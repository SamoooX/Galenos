$(document).ready(function () {
    var rut_med = $("#medicos").val();
    var fechaSeleccionada; 
    function cargarFechasIniciales() {
        $.ajax({
            url: 'https://galenos.samgarrido.repl.co/api/agendas/fechas',
            type: 'POST',
            data: JSON.stringify({
                'rut_med': rut_med
            }),
            contentType: 'application/json',
            success: function (data) {
                cargarFechasEnCarrousel(data.fechas);
            },
            error: function (error) {
                console.log('Error al cargar las fechas disponibles.');
                console.log(error);
            }
        });
    }

    function cargarFechasEnCarrousel(fechas) {
        var dateCarousel = $(".carousel-inner");
        dateCarousel.empty();
        var groupCounter = 0;

        // Divide las fechas en grupos de 5
        for (var i = 0; i < fechas.length; i++) {
            var fecha = fechas[i];

            // Crea un nuevo grupo de fechas si se han agregado 5
            if (i % 5 === 0) {
                groupCounter++;
                var dateItem = $("<div>").addClass("carousel-item text-center");
                if (groupCounter === 1) {
                    dateItem.addClass("active");
                }
                dateCarousel.append(dateItem);
            }
            var dateItem = dateCarousel.children().eq(groupCounter - 1);
            var div = $("<div>").addClass("row row-cols-1 row-cols-md-3 g-4");
            var col = $("<div>").addClass("col text-center");
            var card = $("<div>").addClass("card me-3 mb-3");
            var cardBody = $("<div>").addClass("card-body");
            var cardText = $("<div>").addClass("card-text");
            cardText.text(fecha);
            cardBody.append(cardText);
            card.append(cardBody);
            col.append(card)
            div.append(col)
            dateItem.append(div);

            card.on("click", function() {
                fechaSeleccionada = $(this).find(".card-body").text();
                // Llama a la función para cargar las horas disponibles con la fecha seleccionada
                cargarHorasDisponibles(fechaSeleccionada, rut_med);
              });
        }
    }




    // Función para cargar horas disponibles
    function cargarHorasDisponibles(fecha, rut_med) {

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
    $("#medicos").change(function () {
        rut_med = $(this).val();
        cargarFechasIniciales();
    });

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
        var fecha = fechaSeleccionada; // Obtener el valor de la fecha
        var hora = $("#hora").val(); // Obtener el valor de la hora
        var email_pac = 'mat.aninir@duocuc.cl';

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
            'costo': 15000,
            'estado': false,
            'cancelado': false
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
                enviarCorreo(fecha, hora, email_pac);
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

    function enviarCorreo(fecha, hora, correo){
        var data = {
            service_id: 'service_6t4foot',
            template_id: 'template_roz16eg',
            user_id: 'RKVwpR7cbKFlRY4IS',
            template_params: {
                'to_name': 'Paciente',
                'from_name': 'Samuel',
                'reply_to': correo,
                'message': 'Fecha de atención' + fecha +'Hora de atención' + hora
            }
        };
        
        $.ajax('https://api.emailjs.com/api/v1.0/email/send', {
            type: 'POST',
            data: JSON.stringify(data),
            contentType: 'application/json'
        }).done(function() {
            alert('Tu correo electrónico se ha enviado correctamente.');
        }).fail(function(error) {
            alert('¡Ups! ' + JSON.stringify(error));
        });
    }
});
